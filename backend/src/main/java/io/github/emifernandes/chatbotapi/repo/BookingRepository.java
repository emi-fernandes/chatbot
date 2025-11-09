package io.github.emifernandes.chatbotapi.repo;

import io.github.emifernandes.chatbotapi.domain.Booking;
import org.springframework.data.jpa.repository.JpaRepository;

public interface BookingRepository extends JpaRepository<Booking, Long> {}
