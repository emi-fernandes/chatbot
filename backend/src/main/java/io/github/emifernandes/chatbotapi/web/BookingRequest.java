package io.github.emifernandes.chatbotapi.web;

import java.time.LocalDate;

public record BookingRequest(String origem, String destino, LocalDate data) {}
