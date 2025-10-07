package io.github.emifernandes.chatbotapi.services;

import io.github.emifernandes.chatbotapi.services.dto.VooOffer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class VooSearchService {

    @Value("${tequila.apiKey:}")
    private String apiKey;

    public List<VooOffer> search(String from, String to, String date) {
        // Sem integração externa por enquanto (stub):
        return List.of(
            new VooOffer("DEMO", 799.90, from + " " + date + " 08:00", to + " " + date + " 09:10"),
            new VooOffer("DEMO", 899.50, from + " " + date + " 19:00", to + " " + date + " 20:15")
        );
    }
}
