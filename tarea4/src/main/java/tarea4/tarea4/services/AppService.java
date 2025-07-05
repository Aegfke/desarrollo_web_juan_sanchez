package tarea4.tarea4.services;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.security.MessageDigest;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Formatter;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.cglib.core.Local;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.util.ResourceUtils;
import org.springframework.web.multipart.MultipartFile;

import tarea4.tarea4.models.Activity;
import tarea4.tarea4.models.ActivitiesRepository;
import tarea4.tarea4.models.Nota;
import tarea4.tarea4.models.NotaRepository;
import tarea4.tarea4.models.Tema;
import tarea4.tarea4.models.TemaRepository;

@Service
public class AppService {

    private final String pathStatic;
    private final ActivitiesRepository activitiesRepository;
    private final NotaRepository notaRepository;
    private final TemaRepository temaRepository;

    public AppService(ActivitiesRepository activitiesRepository, NotaRepository notaRepository, TemaRepository temaRepository) throws IOException {
        this.activitiesRepository = activitiesRepository;
        this.notaRepository = notaRepository;
        this.temaRepository = temaRepository;
        // Dynamically resolve the absolute path for the static directory
        Path staticDir = Paths.get(ResourceUtils.getFile("classpath:static").getAbsolutePath());
        this.pathStatic = staticDir.toString();
        System.out.println("Static path resolved to: " + this.pathStatic);
    }


    public List<Map<String, String>> getActivitiesData(Integer pageNumber, Integer pageSize) {
        List<Activity> activities = activitiesRepository.findAllByOrderByIdDesc(PageRequest.of(pageNumber, pageSize)).getContent();
        List<Map<String, String>> activitiesData = new ArrayList<>();

        LocalDateTime ahora = LocalDateTime.now();

        for (Activity act : activities) {
            if (act.getHoraInicio().isAfter(ahora)) {
                continue;
            }
            Map<String, String> actData = new HashMap<>();
            actData.put("id", act.getId().toString());
            actData.put("fecha_inicio", act.getHoraInicio().toString());
            actData.put("sector", act.getSector().toString());
            actData.put("nombre", act.getNombre().toString());

            List<Tema> temas = temaRepository.findByActividadId(act.getId());
            actData.put("tema", temas.get(0).getTema().toString());

            activitiesData.add(actData);
        }

        return activitiesData;


    }

    public void handlePostRequest(
        Integer act_id,
        Integer nota) throws Exception {

            if (Nota.validateNota(nota)){
                //save nota in database

                Nota newNota = new Nota(
                    act_id,
                    nota
                );
                notaRepository.save(newNota);
                System.out.println("Nota saved successfully.");

            } else {
                throw new IllegalArgumentException("Nota validation failed");
            }
        }
    
}
