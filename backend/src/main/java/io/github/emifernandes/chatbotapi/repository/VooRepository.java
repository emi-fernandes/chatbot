package io.github.emifernandes.chatbotapi.repository;

import io.github.emifernandes.chatbotapi.models.Voo;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface VooRepository extends JpaRepository<Voo, Long> { }
