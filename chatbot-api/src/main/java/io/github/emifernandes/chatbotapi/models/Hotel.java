package io.github.emifernandes.chatbotapi.models;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import java.math.BigDecimal;

@Entity
public class Hotel {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Size(max = 120)
    private String name;

    @NotBlank @Size(min = 2, max = 80)
    private String city;

    @NotBlank @Pattern(regexp = "^20\\d{2}-\\d{2}-\\d{2}$")
    private String checkin;

    @NotBlank @Pattern(regexp = "^20\\d{2}-\\d{2}-\\d{2}$")
    private String checkout;

    @DecimalMin("0.0") @Digits(integer = 10, fraction = 2)
    private BigDecimal priceBRL;

    public Hotel() {}
    public Hotel(String name, String city, String checkin, String checkout, BigDecimal priceBRL) {
        this.name = name; this.city = city; this.checkin = checkin; this.checkout = checkout; this.priceBRL = priceBRL;
    }

    public Long getId() { return id; }
    public String getName() { return name; }
    public String getCity() { return city; }
    public String getCheckin() { return checkin; }
    public String getCheckout() { return checkout; }
    public BigDecimal getPriceBRL() { return priceBRL; }

    public void setId(Long id) { this.id = id; }
    public void setName(String v) { this.name = v; }
    public void setCity(String v) { this.city = v; }
    public void setCheckin(String v) { this.checkin = v; }
    public void setCheckout(String v) { this.checkout = v; }
    public void setPriceBRL(BigDecimal v) { this.priceBRL = v; }
}
