package com.vanna.backend.controller;

import com.vanna.backend.dto.*;
import com.vanna.backend.service.VannaService;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class VannaController {
    
    private static final Logger logger = LoggerFactory.getLogger(VannaController.class);
    
    private final VannaService vannaService;
    
    public VannaController(VannaService vannaService) {
        this.vannaService = vannaService;
    }
    
    @GetMapping("/health")
    public ResponseEntity<ApiResponse> health() {
        return ResponseEntity.ok(new ApiResponse(true, "Backend is healthy"));
    }
    
    @PostMapping("/train/ddl")
    public ResponseEntity<ApiResponse> trainDDL(@Valid @RequestBody TrainDDLRequest request) {
        logger.info("Received request to train with DDL");
        ApiResponse response = vannaService.trainWithDDL(request);
        return ResponseEntity.ok(response);
    }
    
    @PostMapping("/train/documentation")
    public ResponseEntity<ApiResponse> trainDocumentation(@Valid @RequestBody TrainDocumentationRequest request) {
        logger.info("Received request to train with documentation");
        ApiResponse response = vannaService.trainWithDocumentation(request);
        return ResponseEntity.ok(response);
    }
    
    @PostMapping("/train/sql")
    public ResponseEntity<ApiResponse> trainSQL(@Valid @RequestBody TrainSQLRequest request) {
        logger.info("Received request to train with SQL example");
        ApiResponse response = vannaService.trainWithSQL(request);
        return ResponseEntity.ok(response);
    }
    
    @PostMapping("/ask")
    public ResponseEntity<ApiResponse> askQuestion(@Valid @RequestBody AskQuestionRequest request) {
        logger.info("Received question: {}", request.getQuestion());
        ApiResponse response = vannaService.askQuestion(request);
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/training-data")
    public ResponseEntity<ApiResponse> getTrainingData() {
        logger.info("Received request to fetch training data");
        ApiResponse response = vannaService.getTrainingData();
        return ResponseEntity.ok(response);
    }
}
