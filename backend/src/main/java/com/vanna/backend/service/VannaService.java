package com.vanna.backend.service;

import com.vanna.backend.dto.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

@Service
public class VannaService {
    
    private static final Logger logger = LoggerFactory.getLogger(VannaService.class);
    
    private final RestTemplate restTemplate;
    
    @Value("${vanna.service.url:http://vanna-service:5000}")
    private String vannaServiceUrl;
    
    public VannaService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }
    
    public ApiResponse trainWithDDL(TrainDDLRequest request) {
        try {
            logger.info("Training Vanna with DDL");
            
            Map<String, String> body = new HashMap<>();
            body.put("ddl", request.getDdl());
            
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            
            HttpEntity<Map<String, String>> entity = new HttpEntity<>(body, headers);
            
            ResponseEntity<Map> response = restTemplate.exchange(
                vannaServiceUrl + "/train/ddl",
                HttpMethod.POST,
                entity,
                Map.class
            );
            
            if (response.getStatusCode().is2xxSuccessful()) {
                logger.info("Successfully trained with DDL");
                return new ApiResponse(true, "DDL trained successfully", response.getBody());
            } else {
                logger.error("Failed to train with DDL: {}", response.getStatusCode());
                return new ApiResponse(false, "Failed to train with DDL");
            }
        } catch (Exception e) {
            logger.error("Error training with DDL: {}", e.getMessage(), e);
            return new ApiResponse(false, "Error: " + e.getMessage());
        }
    }
    
    public ApiResponse trainWithDocumentation(TrainDocumentationRequest request) {
        try {
            logger.info("Training Vanna with documentation");
            
            Map<String, String> body = new HashMap<>();
            body.put("documentation", request.getDocumentation());
            
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            
            HttpEntity<Map<String, String>> entity = new HttpEntity<>(body, headers);
            
            ResponseEntity<Map> response = restTemplate.exchange(
                vannaServiceUrl + "/train/documentation",
                HttpMethod.POST,
                entity,
                Map.class
            );
            
            if (response.getStatusCode().is2xxSuccessful()) {
                logger.info("Successfully trained with documentation");
                return new ApiResponse(true, "Documentation trained successfully", response.getBody());
            } else {
                logger.error("Failed to train with documentation: {}", response.getStatusCode());
                return new ApiResponse(false, "Failed to train with documentation");
            }
        } catch (Exception e) {
            logger.error("Error training with documentation: {}", e.getMessage(), e);
            return new ApiResponse(false, "Error: " + e.getMessage());
        }
    }
    
    public ApiResponse trainWithSQL(TrainSQLRequest request) {
        try {
            logger.info("Training Vanna with SQL example");
            
            Map<String, String> body = new HashMap<>();
            body.put("question", request.getQuestion());
            body.put("sql", request.getSql());
            
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            
            HttpEntity<Map<String, String>> entity = new HttpEntity<>(body, headers);
            
            ResponseEntity<Map> response = restTemplate.exchange(
                vannaServiceUrl + "/train/sql",
                HttpMethod.POST,
                entity,
                Map.class
            );
            
            if (response.getStatusCode().is2xxSuccessful()) {
                logger.info("Successfully trained with SQL example");
                return new ApiResponse(true, "SQL example trained successfully", response.getBody());
            } else {
                logger.error("Failed to train with SQL: {}", response.getStatusCode());
                return new ApiResponse(false, "Failed to train with SQL");
            }
        } catch (Exception e) {
            logger.error("Error training with SQL: {}", e.getMessage(), e);
            return new ApiResponse(false, "Error: " + e.getMessage());
        }
    }
    
    public ApiResponse askQuestion(AskQuestionRequest request) {
        try {
            logger.info("Asking question to Vanna: {}", request.getQuestion());
            
            Map<String, String> body = new HashMap<>();
            body.put("question", request.getQuestion());
            
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            
            HttpEntity<Map<String, String>> entity = new HttpEntity<>(body, headers);
            
            ResponseEntity<Map> response = restTemplate.exchange(
                vannaServiceUrl + "/ask",
                HttpMethod.POST,
                entity,
                Map.class
            );
            
            if (response.getStatusCode().is2xxSuccessful()) {
                logger.info("Successfully received answer from Vanna");
                return new ApiResponse(true, "Question answered successfully", response.getBody());
            } else {
                logger.error("Failed to get answer: {}", response.getStatusCode());
                return new ApiResponse(false, "Failed to get answer");
            }
        } catch (Exception e) {
            logger.error("Error asking question: {}", e.getMessage(), e);
            return new ApiResponse(false, "Error: " + e.getMessage());
        }
    }
    
    public ApiResponse getTrainingData() {
        try {
            logger.info("Fetching training data from Vanna");
            
            ResponseEntity<Map> response = restTemplate.getForEntity(
                vannaServiceUrl + "/training-data",
                Map.class
            );
            
            if (response.getStatusCode().is2xxSuccessful()) {
                logger.info("Successfully fetched training data");
                return new ApiResponse(true, "Training data retrieved successfully", response.getBody());
            } else {
                logger.error("Failed to fetch training data: {}", response.getStatusCode());
                return new ApiResponse(false, "Failed to fetch training data");
            }
        } catch (Exception e) {
            logger.error("Error fetching training data: {}", e.getMessage(), e);
            return new ApiResponse(false, "Error: " + e.getMessage());
        }
    }
}
