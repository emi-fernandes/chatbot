package io.github.emifernandes.chatbotapi.services;

import io.github.emifernandes.chatbotapi.services.dto.HotelOffer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class HotelSearchService {

    @Value("${hotel.provider:stub}")
    private String provider;

    public List<HotelOffer> search(String city, String checkin, String checkout) {
        // Stub de ofertas
        return List.of(
            new HotelOffer("Demo Hotel Center", city, checkin, checkout, 520.50, provider),
            new HotelOffer("Demo Boutique", city, checkin, checkout, 629.90, provider)
        );
    }
}
