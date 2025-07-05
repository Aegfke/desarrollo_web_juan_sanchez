package tarea4.tarea4.controllers;

import org.springframework.web.bind.annotation.RestController;

import tarea4.tarea4.services.ApiService;
import tarea4.tarea4.models.Nota;

import java.util.List;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@RestController
public class ApiController {
    private final ApiService apiService;
    public ApiController(ApiService apiService) {
        this.apiService = apiService;
    }

    @GetMapping("/get-activity-note/{act_id}")
    public Map<String, List<Nota>> getActivitiesEndpoint(@PathVariable("act_id") String act_id) {
        List<Nota> notes = apiService.getNotas(act_id);
        return Map.of("data", notes);
    }

}
