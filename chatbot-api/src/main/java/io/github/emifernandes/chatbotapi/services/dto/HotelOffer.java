package io.github.emifernandes.chatbotapi.services.dto;

public record HotelOffer(
        String name,
        String city,
        String checkin,
        String checkout,
        double priceBRL,
        String provider
) {}
