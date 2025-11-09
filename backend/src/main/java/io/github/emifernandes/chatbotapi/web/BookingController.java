package io.github.emifernandes.chatbotapi.web;

import io.github.emifernandes.chatbotapi.domain.Booking;
import io.github.emifernandes.chatbotapi.repo.BookingRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
public class BookingController {

    private final BookingRepository repo;

    public BookingController(BookingRepository repo) {
        this.repo = repo;
    }

    @PostMapping("/booking")
    public ResponseEntity<?> create(@RequestBody BookingRequest req) {
        Booking b = new Booking();
        b.setOrigem(req.origem());
        b.setDestino(req.destino());
        b.setData(req.data());
        Booking saved = repo.save(b);
        return ResponseEntity.ok(saved);
    }
}
