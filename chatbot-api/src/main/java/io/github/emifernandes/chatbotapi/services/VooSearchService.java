package io.github.emifernandes.chatbotapi.services;

import io.github.emifernandes.chatbotapi.services.dto.VooOffer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.List;

@Service
public class VooSearchService {

    @Value("${tequila.apiKey:}")
    private String apiKey;

    public List<VooOffer> search(String from, String to, String dateIso) {
        // Stub: retorna ofertas de exemplo
        return List.of(
            new VooOffer("DEMO", new BigDecimal("799.90"), from+" "+dateIso+" 08:00", to+" "+dateIso+" 09:10"),
            new VooOffer("DEMO", new BigDecimal("899.50"), from+" "+dateIso+" 19:00", to+" "+dateIso+" 20:15")
        );
    }
}
