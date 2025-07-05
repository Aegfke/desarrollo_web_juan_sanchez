package tarea4.tarea4.services;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import org.springframework.stereotype.Service;

import tarea4.tarea4.models.ActivitiesRepository;
import tarea4.tarea4.models.NotaRepository;
import tarea4.tarea4.models.Nota;

@Service
public class ApiService {
    private final ActivitiesRepository activitiesRepository;
    private final NotaRepository notaRepository;
    public ApiService(ActivitiesRepository activitiesRepository, NotaRepository notaRepository) {
        this.activitiesRepository = activitiesRepository;
        this.notaRepository = notaRepository;
    }

    public List<Nota> getNotas(String act_id) {
        List<Nota> notas = notaRepository.findAll();
        List<Nota> act_notas = new ArrayList<Nota>();
        for (Nota nota : notas) {
            if(nota.getActividadId().toString().equals(act_id)) {
                act_notas.add(nota);
            }
        }
        return act_notas;
    }

    
}
