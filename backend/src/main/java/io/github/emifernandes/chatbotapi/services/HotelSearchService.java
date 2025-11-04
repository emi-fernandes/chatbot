package io.github.emifernandes.chatbotapi.services;

import io.github.emifernandes.chatbotapi.services.dto.HotelOffer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.List;

@Service
public class HotelSearchService {

    @Value("${hotel.provider:stub}")
    private String provider;

    public List<HotelOffer> search(String city, String checkinIso, String checkoutIso) {
        return List.of(
            new HotelOffer("Demo Hotel Center", city, checkinIso, checkoutIso, new BigDecimal("520.50"), provider),
            new HotelOffer("Demo Boutique", city, checkinIso, checkoutIso, new BigDecimal("629.90"), provider)
        );
    }
}
