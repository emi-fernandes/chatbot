package io.github.emifernandes.chatbotapi.controllers;

import org.springframework.http.*;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.*;
import jakarta.validation.ConstraintViolationException;

import java.util.*;

@ControllerAdvice
public class RestExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String,Object>> handleValidation(MethodArgumentNotValidException ex) {
        Map<String,Object> body = new LinkedHashMap<>();
        body.put("error","validation");
        body.put("messages", ex.getBindingResult().getFieldErrors()
                .stream().map(f -> f.getField()+": "+f.getDefaultMessage()).toList());
        return ResponseEntity.badRequest().body(body);
    }

    @ExceptionHandler(ConstraintViolationException.class)
    public ResponseEntity<Map<String,Object>> handleConstraint(ConstraintViolationException ex) {
        Map<String,Object> body = new LinkedHashMap<>();
        body.put("error","constraint");
        body.put("messages", ex.getConstraintViolations().stream()
                .map(v -> v.getPropertyPath()+": "+v.getMessage()).toList());
        return ResponseEntity.badRequest().body(body);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<Map<String,Object>> handleGeneric(Exception ex) {
        Map<String,Object> body = Map.of("error","server", "message", ex.getMessage());
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(body);
    }
}
