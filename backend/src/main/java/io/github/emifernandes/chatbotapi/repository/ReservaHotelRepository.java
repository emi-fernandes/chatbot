package io.github.emifernandes.chatbotapi.repository;

import io.github.emifernandes.chatbotapi.models.ReservaHotel;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ReservaHotelRepository extends JpaRepository<ReservaHotel, Long> { }
