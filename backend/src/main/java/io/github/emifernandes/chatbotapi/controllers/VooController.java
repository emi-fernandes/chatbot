package io.github.emifernandes.chatbotapi.controllers;

import io.github.emifernandes.chatbotapi.models.Voo;
import io.github.emifernandes.chatbotapi.repository.VooRepository;
import io.github.emifernandes.chatbotapi.services.VooSearchService;
import io.github.emifernandes.chatbotapi.services.dto.VooOffer;
import jakarta.validation.Valid;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.time.LocalDate;
import java.util.List;

@RestController
@RequestMapping("/voos")
public class VooController {

    private final VooRepository repo;
    private final VooSearchService service;

    public VooController(VooRepository repo, VooSearchService service) {
        this.repo = repo; this.service = service;
    }

    
    @GetMapping public ResponseEntity<List<Voo>> list() { return ResponseEntity.ok(repo.findAll()); }

    @GetMapping("/{id}")
    public ResponseEntity<Voo> get(@PathVariable Long id) {
        return repo.findById(id).map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<Voo> create(@Valid @RequestBody Voo voo) {
        Voo saved = repo.save(voo);
        return ResponseEntity.created(URI.create("/voos/" + saved.getId())).body(saved);
    }

    @GetMapping("/search")
    public ResponseEntity<List<VooOffer>> search(@RequestParam String from,
                                                 @RequestParam String to,
                                                 @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate date) {
        return ResponseEntity.ok(service.search(from.toUpperCase(), to.toUpperCase(), date.toString()));
    }
}
