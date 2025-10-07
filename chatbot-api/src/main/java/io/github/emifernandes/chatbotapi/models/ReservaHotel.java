package io.github.emifernandes.chatbotapi.models;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import java.math.BigDecimal;
import java.time.*;

@Entity
public class ReservaHotel {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank
    private String city;

    @NotNull
    private LocalDate checkin;

    @NotNull
    private LocalDate checkout;

    @NotBlank
    private String hotelName;

    @DecimalMin("0.0") @Digits(integer=10, fraction=2)
    private BigDecimal priceBRL;

    private String guestName;

    private LocalDateTime createdAt = LocalDateTime.now();

    public Long getId() { return id; }
    public String getCity() { return city; }
    public LocalDate getCheckin() { return checkin; }
    public LocalDate getCheckout() { return checkout; }
    public String getHotelName() { return hotelName; }
    public BigDecimal getPriceBRL() { return priceBRL; }
    public String getGuestName() { return guestName; }
    public LocalDateTime getCreatedAt() { return createdAt; }

    public void setId(Long id) { this.id = id; }
    public void setCity(String v) { this.city = v; }
    public void setCheckin(LocalDate v) { this.checkin = v; }
    public void setCheckout(LocalDate v) { this.checkout = v; }
    public void setHotelName(String v) { this.hotelName = v; }
    public void setPriceBRL(BigDecimal v) { this.priceBRL = v; }
    public void setGuestName(String v) { this.guestName = v; }
}
