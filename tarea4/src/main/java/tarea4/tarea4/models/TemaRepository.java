package tarea4.tarea4.models;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TemaRepository extends JpaRepository<Tema, Integer>{
    List<Tema> findByActividadId(Integer actividadId);
}
