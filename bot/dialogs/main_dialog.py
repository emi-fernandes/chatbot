import re
import asyncio
from typing import Optional
from datetime import datetime

import aiohttp
from botbuilder.core import MessageFactory, TurnContext, StatePropertyAccessor
from botbuilder.dialogs import (
    ComponentDialog,
    DialogSet,
    DialogTurnStatus,
    WaterfallDialog,
    WaterfallStepContext,
    TextPrompt,
    PromptOptions,
)
from botbuilder.schema import SuggestedActions, CardAction, ActionTypes

from config import DefaultConfig

CFG = DefaultConfig()

IATA_RE = re.compile(r"^[A-Za-z]{3}$")
DATE_FMTS = ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d")  

def normalize_iata(x: str) -> str:
    return (x or "").strip().upper()

def normalize_city(x: str) -> str:
    return (x or "").strip().title()

def parse_date_any(s: str) -> Optional[datetime]:
    s = (s or "").strip()
    for fmt in DATE_FMTS:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None

def fmt_br(dt: datetime) -> str:
    return dt.strftime("%d/%m/%Y")

def fmt_iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")  # ISO yyyy-MM-dd (para a API Java)

def is_cancel(t: str) -> bool:
    return (t or "").strip().lower() in {"cancelar", "cancel", "sair"}

def is_restart(t: str) -> bool:
    return (t or "").strip().lower() in {"reiniciar", "reset", "recomeçar"}

def menu_message(text: str = "Como posso ajudar?"):
    from bot.main_bot import make_menu
    return make_menu(text)

class MainDialog(ComponentDialog):
    def __init__(self, user_state):
        super().__init__(MainDialog.__name__)

    
        self.add_dialog(TextPrompt("TextPrompt"))

        self.add_dialog(WaterfallDialog("VooFlow", [
            self.voo_step_origem,
            self.voo_step_destino,
            self.voo_step_data,
            self.voo_step_confirm,
            self.voo_step_nome,     
            self.voo_step_busca,
        ]))

    
        self.add_dialog(WaterfallDialog("HotelFlow", [
            self.hotel_step_cidade,
            self.hotel_step_checkin,
            self.hotel_step_checkout,
            self.hotel_step_confirm,
            self.hotel_step_nome,   
            self.hotel_step_busca,
        ]))

     
        self.add_dialog(WaterfallDialog("ManageFlow", [
            self.manage_step_tipo,
            self.manage_step_listar,
            self.manage_step_confirmar,
            self.manage_step_cancelar,
        ]))

    
        self.add_dialog(WaterfallDialog("Root", [self.route_step]))
        self.initial_dialog_id = "Root"

    async def run(self, turn_context: TurnContext, accessor: StatePropertyAccessor):
        txt = (turn_context.activity.text or "").strip()
        if is_cancel(txt):
            await turn_context.send_activity("👍 Fluxo cancelado.")
            await turn_context.send_activity(menu_message())
            return
        if is_restart(txt):
            await turn_context.send_activity("🔄 Recomeçando…")

        dialog_set = DialogSet(accessor)
        dialog_set.add(self)
        dc = await dialog_set.create_context(turn_context)
        result = await dc.continue_dialog()
        if result.status == DialogTurnStatus.Empty:
            await dc.begin_dialog(self.id)

    async def route_step(self, step: WaterfallStepContext):
        text = (step.context.activity.text or "").strip()
        tokens = text.split()

        if len(tokens) >= 1 and tokens[0].lower() == "voo":
            if len(tokens) >= 4:
                step.values["origem"] = tokens[1]
                step.values["destino"] = tokens[2]
                step.values["data_raw"] = tokens[3]
            return await step.begin_dialog("VooFlow")

        if len(tokens) >= 1 and tokens[0].lower() == "hotel":
            if len(tokens) >= 4:
                if len(tokens) > 4:
                
                    step.values["cidade"] = " ".join(tokens[1:-2])
                    step.values["checkin_raw"] = tokens[-2]
                    step.values["checkout_raw"] = tokens[-1]
                else:
                    step.values["cidade"] = tokens[1]
                    step.values["checkin_raw"] = tokens[2]
                    step.values["checkout_raw"] = tokens[3]
            return await step.begin_dialog("HotelFlow")

        t = text.lower()
        if t in {"consultas", "consulta", "cancelamentos", "cancelamento", "📋 consultas e cancelamentos"}:
            return await step.begin_dialog("ManageFlow")


        if t in {"ajuda", "/ajuda", "help", "/help"}:
            await step.context.send_activity(
                "Comandos:\n"
                "• `voo ORIGEM DESTINO DATA(DD/MM/AAAA)`\n"
                "• `hotel CIDADE CHECKIN(DD/MM/AAAA) CHECKOUT(DD/MM/AAAA)`\n"
                "• `consultas` para listar/cancelar\n"
                "• `menu` para ver botões"
            )
            await step.context.send_activity(menu_message("O que deseja fazer agora?"))
            return await step.end_dialog()

    
        if t in {"menu", "/menu"}:
            await step.context.send_activity(menu_message())
            return await step.end_dialog()

     
        await step.context.send_activity(
            "Digite:\n"
            "• `voo ORIGEM DESTINO DATA(DD/MM/AAAA)`\n"
            "• `hotel CIDADE CHECKIN(DD/MM/AAAA) CHECKOUT(DD/MM/AAAA)`\n"
            "• ou clique nos botões abaixo."
        )
        await step.context.send_activity(menu_message())
        return await step.end_dialog()


    async def voo_step_origem(self, step: WaterfallStepContext):
        v = normalize_iata(step.values.get("origem", ""))
        if v and IATA_RE.match(v):
            return await step.next(v)
        return await step.prompt("TextPrompt", PromptOptions(prompt=MessageFactory.text("Origem (IATA, ex.: **GIG**) ?")))

    async def voo_step_destino(self, step: WaterfallStepContext):
        step.values["origem"] = normalize_iata(step.result or step.values.get("origem", ""))
        v = normalize_iata(step.values.get("destino", ""))
        if v and IATA_RE.match(v):
            return await step.next(v)
        return await step.prompt("TextPrompt", PromptOptions(prompt=MessageFactory.text("Destino (IATA, ex.: **GRU**) ?")))

    async def voo_step_data(self, step: WaterfallStepContext):
        step.values["destino"] = normalize_iata(step.result or step.values.get("destino", ""))
        raw = step.values.get("data_raw", "")
        if raw:
            return await step.next(raw)
        return await step.prompt("TextPrompt", PromptOptions(prompt=MessageFactory.text("Data (**DD/MM/AAAA**)?")))

    async def voo_step_confirm(self, step: WaterfallStepContext):
        raw = step.result or step.values.get("data_raw", "")
        dt = parse_date_any(raw)
        if not (IATA_RE.match(step.values["origem"]) and IATA_RE.match(step.values["destino"]) and dt):
            await step.context.send_activity("⚠️ Dados inválidos. Exemplo: `voo GIG GRU 02/11/2025`.")
            return await step.end_dialog()

        step.values["data_br"] = fmt_br(dt)
        step.values["data_iso"] = fmt_iso(dt)

        o, d = step.values["origem"], step.values["destino"]
        msg = MessageFactory.text(f"Confirmar busca de voo **{o} → {d}** em **{step.values['data_br']}**?")
        msg.suggested_actions = SuggestedActions(actions=[
            CardAction(title="Sim", type=ActionTypes.im_back, value="sim"),
            CardAction(title="Não", type=ActionTypes.im_back, value="não"),
        ])
        return await step.prompt("TextPrompt", PromptOptions(prompt=msg))

    async def voo_step_nome(self, step: WaterfallStepContext):
        
        if (step.result or "").strip().lower() not in {"sim", "s", "yes", "y"}:
            await step.context.send_activity("❌ Busca cancelada.")
            await step.context.send_activity(menu_message())
            return await step.end_dialog()

        if CFG.SAVE_TO_DB:
            default_name = (step.context.activity.from_property.name or "Cliente") \
                if getattr(step.context.activity, "from_property", None) else "Cliente"
            prompt = MessageFactory.text(f"Qual o **nome do passageiro**? (ex.: {default_name})")
            return await step.prompt("TextPrompt", PromptOptions(prompt=prompt))
        else:
            step.values["passengerName"] = "Cliente"
            return await step.next("Cliente")

    async def voo_step_busca(self, step: WaterfallStepContext):
    
        if step.result is not None:
            name = (step.result or "").strip() or "Cliente"
            step.values["passengerName"] = name

        o = step.values["origem"]
        d = step.values["destino"]
        date_iso = step.values["data_iso"]

        offers = await self._call_get("/voos/search", {"from": o, "to": d, "date": date_iso})
        if isinstance(offers, str):
            await step.context.send_activity(offers)
            return await step.end_dialog()
        if not offers:
            await step.context.send_activity("Não encontrei ofertas de voo.")
            return await step.end_dialog()

        lines = [
            f"✈️ {o_.get('airline','?')} • R$ {float(o_.get('priceBRL',0)):.2f} • {o_.get('departure','?')} → {o_.get('arrival','?')}"
            for o_ in offers[:3]
        ]
        await step.context.send_activity("Ofertas de voo:\n" + "\n".join(lines))

        if CFG.SAVE_TO_DB:
            best = offers[0]
            payload = {
                "origin": o,
                "destination": d,
                "date": date_iso,
                "airline": best.get("airline", "DEMO"),
                "priceBRL": str(best.get("priceBRL", "0")),
                "passengerName": step.values.get("passengerName", "Cliente"),
            }
            res = await self._call_post("/reservas/voos", payload)
            if isinstance(res, dict) and res.get("id"):
                await step.context.send_activity(
                    f"✅ Reserva de **voo** criada! ID **{res['id']}** para **{payload['passengerName']}**."
                )
            else:
                await step.context.send_activity(
                    res if isinstance(res, str) else "⚠️ Falha ao salvar a reserva de voo."
                )

        return await step.end_dialog()

    async def hotel_step_cidade(self, step: WaterfallStepContext):
        v = normalize_city(step.values.get("cidade", ""))
        if v:
            return await step.next(v)
        return await step.prompt("TextPrompt", PromptOptions(prompt=MessageFactory.text("Cidade? (ex.: **Lisboa**)")))

    async def hotel_step_checkin(self, step: WaterfallStepContext):
        step.values["cidade"] = normalize_city(step.result or step.values.get("cidade", ""))
        raw = step.values.get("checkin_raw", "")
        if raw:
            return await step.next(raw)
        return await step.prompt("TextPrompt", PromptOptions(prompt=MessageFactory.text("Check-in (**DD/MM/AAAA**)?")))

    async def hotel_step_checkout(self, step: WaterfallStepContext):
        step.values["checkin_raw"] = step.result or step.values.get("checkin_raw", "")
        raw = step.values.get("checkout_raw", "")
        if raw:
            return await step.next(raw)
        return await step.prompt("TextPrompt", PromptOptions(prompt=MessageFactory.text("Check-out (**DD/MM/AAAA**)?")))

    async def hotel_step_confirm(self, step: WaterfallStepContext):
        step.values["checkout_raw"] = step.result or step.values.get("checkout_raw", "")
        dt_in = parse_date_any(step.values["checkin_raw"])
        dt_out = parse_date_any(step.values["checkout_raw"])

        if not (dt_in and dt_out and dt_out > dt_in):
            await step.context.send_activity("⚠️ Datas inválidas. Use **DD/MM/AAAA** e garanta check-out > check-in.")
            return await step.end_dialog()

        step.values["checkin_br"] = fmt_br(dt_in)
        step.values["checkout_br"] = fmt_br(dt_out)
        step.values["checkin_iso"] = fmt_iso(dt_in)
        step.values["checkout_iso"] = fmt_iso(dt_out)

        cty = step.values["cidade"]
        msg = MessageFactory.text(
            f"Confirmar busca de hotel em **{cty}** de **{step.values['checkin_br']}** a **{step.values['checkout_br']}**?"
        )
        msg.suggested_actions = SuggestedActions(actions=[
            CardAction(title="Sim", type=ActionTypes.im_back, value="sim"),
            CardAction(title="Não", type=ActionTypes.im_back, value="não"),
        ])
        return await step.prompt("TextPrompt", PromptOptions(prompt=msg))

    async def hotel_step_nome(self, step: WaterfallStepContext):
        if (step.result or "").strip().lower() not in {"sim", "s", "yes", "y"}:
            await step.context.send_activity("❌ Busca cancelada.")
            await step.context.send_activity(menu_message())
            return await step.end_dialog()

        if CFG.SAVE_TO_DB:
            default_name = (step.context.activity.from_property.name or "Cliente") \
                if getattr(step.context.activity, "from_property", None) else "Cliente"
            prompt = MessageFactory.text(f"Qual o **nome do hóspede**? (ex.: {default_name})")
            return await step.prompt("TextPrompt", PromptOptions(prompt=prompt))
        else:
            step.values["guestName"] = "Cliente"
            return await step.next("Cliente")

    async def hotel_step_busca(self, step: WaterfallStepContext):
        if step.result is not None:
            name = (step.result or "").strip() or "Cliente"
            step.values["guestName"] = name

        city = step.values["cidade"]
        ci_iso = step.values["checkin_iso"]
        co_iso = step.values["checkout_iso"]

        offers = await self._call_get("/hoteis/search", {"city": city, "checkin": ci_iso, "checkout": co_iso})
        if isinstance(offers, str):
            await step.context.send_activity(offers)
            return await step.end_dialog()
        if not offers:
            await step.context.send_activity("Não encontrei ofertas de hotel.")
            return await step.end_dialog()

        lines = [
            f"🏨 {o_.get('name','Hotel ?')} • R$ {float(o_.get('priceBRL',0)):.2f} • {o_.get('city', city)}"
            for o_ in offers[:3]
        ]
        await step.context.send_activity("Ofertas de hotel:\n" + "\n".join(lines))

        if CFG.SAVE_TO_DB:
            best = offers[0]
            payload = {
                "city": city,
                "checkin": ci_iso,
                "checkout": co_iso,
                "hotelName": best.get("name", "Hotel"),
                "priceBRL": str(best.get("priceBRL", "0")),
                "guestName": step.values.get("guestName", "Cliente"),
            }
            res = await self._call_post("/reservas/hoteis", payload)
            if isinstance(res, dict) and res.get("id"):
                await step.context.send_activity(
                    f"✅ Reserva de **hotel** criada! ID **{res['id']}** para **{payload['guestName']}**."
                )
            else:
                await step.context.send_activity(
                    res if isinstance(res, str) else "⚠️ Falha ao salvar a reserva de hotel."
                )

        return await step.end_dialog()

    async def manage_step_tipo(self, step: WaterfallStepContext):
        msg = MessageFactory.text("Você quer ver/cancelar **voos** ou **hotéis**?")
        msg.suggested_actions = SuggestedActions(actions=[
            CardAction(title="Voos", type=ActionTypes.im_back, value="voos"),
            CardAction(title="Hotéis", type=ActionTypes.im_back, value="hoteis"),
            CardAction(title="Voltar", type=ActionTypes.im_back, value="voltar"),
        ])
        return await step.prompt("TextPrompt", PromptOptions(prompt=msg))

    async def manage_step_listar(self, step: WaterfallStepContext):
        choice = (step.result or "").strip().lower()
        if choice in {"voltar", "menu"}:
            await step.context.send_activity("↩️ Voltando ao menu.")
            await step.context.send_activity(menu_message())
            return await step.end_dialog()

        if choice not in {"voos", "hoteis"}:
            await step.context.send_activity("⚠️ Opção inválida. Tente **voos** ou **hoteis**.")
            return await step.replace_dialog("ManageFlow")

        step.values["tipo"] = choice

    
        path = "/reservas/voos" if choice == "voos" else "/reservas/hoteis"
        items = await self._call_get(path, {})
        if isinstance(items, str):
            await step.context.send_activity(items)
            return await step.end_dialog()

        if not items:
            await step.context.send_activity("Nenhuma reserva encontrada.")
            return await step.end_dialog()

        linhas = []
        subset = items[:5] if len(items) > 5 else items
        for r in subset:
            if choice == "voos":
                linhas.append(
                    f"ID **{r.get('id')}** • {r.get('origin')}→{r.get('destination')} • {r.get('date')} • {r.get('passengerName','')}"
                )
            else:
                linhas.append(
                    f"ID **{r.get('id')}** • {r.get('city')} • {r.get('checkin')}→{r.get('checkout')} • {r.get('guestName','')}"
                )
        await step.context.send_activity("Reservas encontradas:\n" + "\n".join(linhas))

        prompt = MessageFactory.text("Digite o **ID** para cancelar, ou `voltar` para sair.")
        return await step.prompt("TextPrompt", PromptOptions(prompt=prompt))

    async def manage_step_confirmar(self, step: WaterfallStepContext):
        txt = (step.result or "").strip().lower()
        if txt in {"voltar", "menu"}:
            await step.context.send_activity("↩️ Voltando ao menu.")
            await step.context.send_activity(menu_message())
            return await step.end_dialog()

        if not txt.isdigit():
            await step.context.send_activity("⚠️ ID inválido.")
            return await step.replace_dialog("ManageFlow")

        step.values["id_cancel"] = int(txt)
        msg = MessageFactory.text(f"Confirmar **cancelamento** da reserva ID **{step.values['id_cancel']}**?")
        msg.suggested_actions = SuggestedActions(actions=[
            CardAction(title="Sim", type=ActionTypes.im_back, value="sim"),
            CardAction(title="Não", type=ActionTypes.im_back, value="não"),
        ])
        return await step.prompt("TextPrompt", PromptOptions(prompt=msg))

    async def manage_step_cancelar(self, step: WaterfallStepContext):
        if (step.result or "").strip().lower() not in {"sim", "s", "yes", "y"}:
            await step.context.send_activity("Cancelamento abortado.")
            return await step.end_dialog()

        tipo = step.values.get("tipo")
        _id = step.values.get("id_cancel")
        path = f"/reservas/voos/{_id}" if tipo == "voos" else f"/reservas/hoteis/{_id}"

        res = await self._call_delete(path)
        if res is True:
            await step.context.send_activity(f"🗑️ Reserva **{tipo[:-1]}** ID **{_id}** cancelada com sucesso.")
        else:
            await step.context.send_activity(res if isinstance(res, str) else "⚠️ Falha ao cancelar.")

        return await step.end_dialog()


    async def _call_get(self, path: str, params: dict):
        url = f"{CFG.JAVA_API_BASE}{path}"
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(url, params=params, timeout=20) as r:
                    if r.status != 200:
                        txt = await r.text()
                        return f"⚠️ Erro {r.status} consultando {path}: {txt}"
                    return await r.json()
        except aiohttp.ClientConnectorError:
            return f"⚠️ API indisponível em {CFG.JAVA_API_BASE}."
        except asyncio.TimeoutError:
            return "⚠️ Tempo esgotado consultando a API."
        except Exception as e:
            return f"⚠️ Falha HTTP: {e}"

    async def _call_post(self, path: str, data: dict):
        """Envia POST como form-urlencoded (compatível com @RequestParam no Spring).
        Se seus endpoints usarem @RequestBody, troque para 'json=data'."""
        url = f"{CFG.JAVA_API_BASE}{path}"
        try:
            async with aiohttp.ClientSession() as s:
                async with s.post(url, data=data, timeout=20) as r:   
                    txt = await r.text()
                    print("POST(form)", path, r.status, txt)
                    if r.status in (200, 201):
                        try:
                            return await r.json()
                        except Exception:
                            return {"status": r.status}
                    return f"⚠️ Erro {r.status} no POST {path}: {txt}"
        except aiohttp.ClientConnectorError:
            return f"⚠️ API indisponível em {CFG.JAVA_API_BASE}."
        except asyncio.TimeoutError:
            return "⚠️ Tempo esgotado chamando a API."
        except Exception as e:
            return f"⚠️ Falha HTTP: {e}"

    async def _call_delete(self, path: str):
        url = f"{CFG.JAVA_API_BASE}{path}"
        try:
            async with aiohttp.ClientSession() as s:
                async with s.delete(url, timeout=20) as r:
                    print("DELETE", path, r.status)
                    if r.status in (200, 202, 204):
                        return True
                    txt = await r.text()
                    return f"⚠️ Erro {r.status} no DELETE {path}: {txt}"
        except aiohttp.ClientConnectorError:
            return f"⚠️ API indisponível em {CFG.JAVA_API_BASE}."
        except asyncio.TimeoutError:
            return "⚠️ Tempo esgotado chamando a API."
        except Exception as e:
            return f"⚠️ Falha HTTP: {e}"
