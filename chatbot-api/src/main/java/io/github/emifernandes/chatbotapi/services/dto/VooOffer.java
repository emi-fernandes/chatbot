package io.github.emifernandes.chatbotapi.services.dto;

public record VooOffer(
        String airline,
        double priceBRL,
        String departure,
        String arrival
) {}
