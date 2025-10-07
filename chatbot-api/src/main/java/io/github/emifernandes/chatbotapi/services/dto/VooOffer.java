package io.github.emifernandes.chatbotapi.services.dto;

import java.math.BigDecimal;

public record VooOffer(
        String airline,
        BigDecimal priceBRL,
        String departure,
        String arrival
) {}
