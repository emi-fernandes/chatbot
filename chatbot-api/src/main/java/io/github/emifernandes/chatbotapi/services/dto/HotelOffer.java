package io.github.emifernandes.chatbotapi.services.dto;

import java.math.BigDecimal;

public record HotelOffer(
        String name,
        String city,
        String checkin,
        String checkout,
        BigDecimal priceBRL,
        String provider
) {}
