package io.github.emifernandes.chatbotapi.controllers;

import io.github.emifernandes.chatbotapi.services.CluService;
import io.github.emifernandes.chatbotapi.services.CluService.CluResult;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/chat")
public class ChatController {

    private final CluService cluService;

    public ChatController(CluService cluService) {
        this.cluService = cluService;
    }

    @PostMapping
    public Map<String, Object> chat(@RequestBody Map<String, String> req) throws Exception {

        String userMessage = req.get("message");
        CluResult result = cluService.analyze(userMessage);

        Map<String, Object> resp = new HashMap<>();
        resp.put("intent", result.intent);
        resp.put("entities", result.entitiesJson);

        String reply;

        switch (result.intent) {
            case "ComprarVoo":
                reply = "Certo! Vamos comprar um voo. De onde para onde você quer viajar?";
                break;
            case "ConsultarVoo":
                reply = "Claro! Me informe o código da reserva do seu voo.";
                break;
            case "CancelarVoo":
                reply = "Ok, vou cancelar seu voo. Qual é o código da reserva?";
                break;
            case "ReservarHotel":
                reply = "Vamos reservar um hotel! Qual cidade e datas?";
                break;
            case "ConsultarHotel":
                reply = "Tudo bem. Qual o código da reserva?";
                break;
            case "CancelarHotel":
                reply = "Certo. Me informe o código da reserva que deseja cancelar.";
                break;
            default:
                reply = "Não entendi. Você quer falar sobre voo ou hotel?";
        }

        resp.put("reply", reply);
        return resp;
    }
}
