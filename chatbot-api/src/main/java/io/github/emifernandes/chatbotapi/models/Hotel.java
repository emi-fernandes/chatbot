package io.github.emifernandes.chatbotapi.models;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import java.math.BigDecimal;
import java.time.*;

@Entity
public class Hotel {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Size(max=120)
    private String name;

    @NotBlank @Size(min=2, max=80)
    private String city;

    @NotNull
    private LocalDate checkin;

    @NotNull
    private LocalDate checkout;

    @DecimalMin("0.0") @Digits(integer=10, fraction=2)
    private BigDecimal priceBRL = BigDecimal.ZERO;

    private LocalDateTime createdAt = LocalDateTime.now();

    public Hotel() {}
    public Hotel(String name, String city, LocalDate checkin, LocalDate checkout, BigDecimal price) {
        this.name=name; this.city=city; this.checkin=checkin; this.checkout=checkout; this.priceBRL=price;
    }

    public Long getId() { return id; }
    public String getName() { return name; }
    public String getCity() { return city; }
    public LocalDate getCheckin() { return checkin; }
    public LocalDate getCheckout() { return checkout; }
    public BigDecimal getPriceBRL() { return priceBRL; }
    public LocalDateTime getCreatedAt() { return createdAt; }

    public void setId(Long id) { this.id = id; }
    public void setName(String v) { this.name = v; }
    public void setCity(String v) { this.city = v; }
    public void setCheckin(LocalDate v) { this.checkin = v; }
    public void setCheckout(LocalDate v) { this.checkout = v; }
    public void setPriceBRL(BigDecimal v) { this.priceBRL = v; }
}
