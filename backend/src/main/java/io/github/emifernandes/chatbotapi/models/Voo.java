package io.github.emifernandes.chatbotapi.models;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import java.time.*;

@Entity
public class Voo {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank @Size(max=8)
    private String flightNumber;

    @NotBlank @Pattern(regexp = "^[A-Za-z]{3}$")
    private String origin;

    @NotBlank @Pattern(regexp = "^[A-Za-z]{3}$")
    private String destination;

    @NotNull
    private LocalDate date;

    private LocalDateTime createdAt = LocalDateTime.now();

    public Voo() {}
    public Voo(String flightNumber, String origin, String destination, LocalDate date) {
        this.flightNumber = flightNumber; this.origin = origin; this.destination = destination; this.date = date;
    }

    public Long getId() { return id; }
    public String getFlightNumber() { return flightNumber; }
    public String getOrigin() { return origin; }
    public String getDestination() { return destination; }
    public LocalDate getDate() { return date; }
    public LocalDateTime getCreatedAt() { return createdAt; }

    public void setId(Long id) { this.id = id; }
    public void setFlightNumber(String v) { this.flightNumber = v; }
    public void setOrigin(String v) { this.origin = v; }
    public void setDestination(String v) { this.destination = v; }
    public void setDate(LocalDate v) { this.date = v; }
}
