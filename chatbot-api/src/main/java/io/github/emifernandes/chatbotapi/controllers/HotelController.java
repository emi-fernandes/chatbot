package io.github.emifernandes.chatbotapi.controllers;

import io.github.emifernandes.chatbotapi.models.Hotel;
import io.github.emifernandes.chatbotapi.repository.HotelRepository;
import io.github.emifernandes.chatbotapi.services.HotelSearchService;
import io.github.emifernandes.chatbotapi.services.dto.HotelOffer;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.net.URI;
import java.util.List;

@RestController
@RequestMapping("/hoteis")
public class HotelController {

    private final HotelRepository repo;
    private final HotelSearchService service;

    public HotelController(HotelRepository repo, HotelSearchService service) {
        this.repo = repo; this.service = service;
    }

    @GetMapping
    public ResponseEntity<List<Hotel>> list() {
        return ResponseEntity.ok(repo.findAll());
    }

    @GetMapping("/{id}")
    public ResponseEntity<Hotel> get(@PathVariable Long id) {
        return repo.findById(id).map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<Hotel> create(@Valid @RequestBody Hotel hotel) {
        if (hotel.getCheckout().compareTo(hotel.getCheckin()) <= 0) {
            return ResponseEntity.badRequest().build();
        }
        if (hotel.getPriceBRL() == null) hotel.setPriceBRL(BigDecimal.ZERO);
        Hotel saved = repo.save(hotel);
        return ResponseEntity.created(URI.create("/hoteis/" + saved.getId())).body(saved);
    }

    @GetMapping("/search")
    public ResponseEntity<List<HotelOffer>> search(@RequestParam String city,
                                                   @RequestParam String checkin,
                                                   @RequestParam String checkout) {
        if (checkout.compareTo(checkin) <= 0) return ResponseEntity.badRequest().build();
        return ResponseEntity.ok(service.search(city, checkin, checkout));
    }
}
