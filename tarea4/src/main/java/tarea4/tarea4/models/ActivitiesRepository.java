package tarea4.tarea4.models;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ActivitiesRepository extends JpaRepository<Activity, Long>{
    Page<Activity> findAllByOrderByIdDesc(Pageable pageable);
}

