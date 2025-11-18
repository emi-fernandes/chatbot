package io.github.emifernandes.chatbotapi.services;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

@Service
public class CluService {

    @Value("${azure.language.endpoint}")
    private String endpoint;

    @Value("${azure.language.key}")
    private String key;

    @Value("${azure.language.projectName}")
    private String projectName;

    @Value("${azure.language.deploymentName}")
    private String deploymentName;

    private final RestTemplate restTemplate = new RestTemplate();
    private final ObjectMapper mapper = new ObjectMapper();

    public CluResult analyze(String text) throws Exception {

        String url = endpoint + "/language/:analyze-conversations?api-version=2024-11-01";

        Map<String, Object> body = new HashMap<>();
        body.put("kind", "Conversation");

        Map<String, Object> conversationItem = new HashMap<>();
        conversationItem.put("id", "1");
        conversationItem.put("text", text);
        conversationItem.put("modality", "text");
        conversationItem.put("participantId", "user");

        Map<String, Object> analysisInput = new HashMap<>();
        analysisInput.put("conversationItem", conversationItem);

        Map<String, Object> parameters = new HashMap<>();
        parameters.put("projectName", projectName);
        parameters.put("deploymentName", deploymentName);
        parameters.put("stringIndexType", "TextElement_V8");

        body.put("analysisInput", analysisInput);
        body.put("parameters", parameters);

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.set("Ocp-Apim-Subscription-Key", key);

        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(body, headers);

        ResponseEntity<String> response = restTemplate.exchange(
                url,
                HttpMethod.POST,
                entity,
                String.class
        );

        JsonNode root = mapper.readTree(response.getBody());
        JsonNode prediction = root.path("result").path("prediction");

        CluResult result = new CluResult();
        result.intent = prediction.path("topIntent").asText();
        result.entitiesJson = prediction.path("entities").toString();

        return result;
    }

    public static class CluResult {
        public String intent;
        public String entitiesJson;
    }
}
