package io.github.emifernandes.chatbotapi.models;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import java.math.BigDecimal;
import java.time.*;

@Entity
public class ReservaVoo {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank @Pattern(regexp = "^[A-Za-z]{3}$")
    private String origin;

    @NotBlank @Pattern(regexp = "^[A-Za-z]{3}$")
    private String destination;

    @NotNull
    private LocalDate date;

    @NotBlank
    private String airline;

    @DecimalMin("0.0") @Digits(integer=10, fraction=2)
    private BigDecimal priceBRL;

    private String passengerName;

    private LocalDateTime createdAt = LocalDateTime.now();

    public Long getId() { return id; }
    public String getOrigin() { return origin; }
    public String getDestination() { return destination; }
    public LocalDate getDate() { return date; }
    public String getAirline() { return airline; }
    public BigDecimal getPriceBRL() { return priceBRL; }
    public String getPassengerName() { return passengerName; }
    public LocalDateTime getCreatedAt() { return createdAt; }

    public void setId(Long id) { this.id = id; }
    public void setOrigin(String v) { this.origin = v; }
    public void setDestination(String v) { this.destination = v; }
    public void setDate(LocalDate v) { this.date = v; }
    public void setAirline(String v) { this.airline = v; }
    public void setPriceBRL(BigDecimal v) { this.priceBRL = v; }
    public void setPassengerName(String v) { this.passengerName = v; }
}
