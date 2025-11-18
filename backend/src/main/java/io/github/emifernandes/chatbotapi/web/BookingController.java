package io.github.emifernandes.chatbotapi.web;

import io.github.emifernandes.chatbotapi.domain.Booking;
import io.github.emifernandes.chatbotapi.repo.BookingRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/booking")
public class BookingController {

    private final BookingRepository repo;

    public BookingController(BookingRepository repo) {
        this.repo = repo;
    }

    @PostMapping
    public ResponseEntity<Booking> create(@RequestBody Booking booking) {
        Booking saved = repo.save(booking);
        return ResponseEntity.ok(saved);
    }

    @GetMapping
    public List<Booking> list() {
        return repo.findAll();
    }
}
