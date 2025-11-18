package io.github.emifernandes.chatbotapi.repository;

import io.github.emifernandes.chatbotapi.models.ReservaVoo;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ReservaVooRepository extends JpaRepository<ReservaVoo, Long> { }
