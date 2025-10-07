package io.github.emifernandes.chatbotapi.controllers;

import io.github.emifernandes.chatbotapi.models.*;
import io.github.emifernandes.chatbotapi.repository.*;
import jakarta.validation.Valid;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.net.URI;
import java.time.LocalDate;
import java.util.List;

@RestController
@RequestMapping("/reservas")
public class ReservaController {

    private final ReservaVooRepository vooRepo;
    private final ReservaHotelRepository hotelRepo;

    public ReservaController(ReservaVooRepository vooRepo, ReservaHotelRepository hotelRepo) {
        this.vooRepo = vooRepo; this.hotelRepo = hotelRepo;
    }

    // ---- VOOS ----
    @GetMapping("/voos")
    public ResponseEntity<List<ReservaVoo>> listVoo() { return ResponseEntity.ok(vooRepo.findAll()); }

    @GetMapping("/voos/{id}")
    public ResponseEntity<ReservaVoo> getVoo(@PathVariable Long id) {
        return vooRepo.findById(id).map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }

    @PostMapping("/voos")
    public ResponseEntity<ReservaVoo> createVoo(@RequestParam String origin,
                                                @RequestParam String destination,
                                                @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate date,
                                                @RequestParam String airline,
                                                @RequestParam BigDecimal priceBRL,
                                                @RequestParam(required=false) String passengerName) {
        ReservaVoo r = new ReservaVoo();
        r.setOrigin(origin.toUpperCase());
        r.setDestination(destination.toUpperCase());
        r.setDate(date);
        r.setAirline(airline);
        r.setPriceBRL(priceBRL);
        r.setPassengerName(passengerName);
        ReservaVoo saved = vooRepo.save(r);
        return ResponseEntity.created(URI.create("/reservas/voos/"+saved.getId())).body(saved);
    }

    // ---- HOTEIS ----
    @GetMapping("/hoteis")
    public ResponseEntity<List<ReservaHotel>> listHotel() { return ResponseEntity.ok(hotelRepo.findAll()); }

    @GetMapping("/hoteis/{id}")
    public ResponseEntity<ReservaHotel> getHotel(@PathVariable Long id) {
        return hotelRepo.findById(id).map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }

    @PostMapping("/hoteis")
    public ResponseEntity<ReservaHotel> createHotel(@RequestParam String city,
                                                    @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate checkin,
                                                    @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate checkout,
                                                    @RequestParam String hotelName,
                                                    @RequestParam BigDecimal priceBRL,
                                                    @RequestParam(required=false) String guestName) {
        if (!checkout.isAfter(checkin)) return ResponseEntity.badRequest().build();
        ReservaHotel r = new ReservaHotel();
        r.setCity(city);
        r.setCheckin(checkin);
        r.setCheckout(checkout);
        r.setHotelName(hotelName);
        r.setPriceBRL(priceBRL);
        r.setGuestName(guestName);
        ReservaHotel saved = hotelRepo.save(r);
        return ResponseEntity.created(URI.create("/reservas/hoteis/"+saved.getId())).body(saved);
    }
}
