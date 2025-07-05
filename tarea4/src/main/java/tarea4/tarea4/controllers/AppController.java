package tarea4.tarea4.controllers;

import java.util.List;
import java.util.Map;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import tarea4.tarea4.services.AppService;

@Controller
public class AppController {
    private final AppService appService;
    public AppController(AppService appService) {
        this.appService = appService;
    }

    @GetMapping("/")
    public String indexRoute(
        @RequestParam(defaultValue = "0") int pagenumber,
        @RequestParam(defaultValue = "10") int pagesize,
        Model model) {
        List<Map<String, String>> modelData = appService.getActivitiesData(pagenumber, pagesize);
        model.addAttribute("currentPage", pagenumber);
        model.addAttribute("data", modelData);
        return "index";
    }

    @GetMapping("/post-nota/{act_id}")
    public String postRoute(@PathVariable Integer act_id, Model model) {
        return "evaluar";
    }


    @PostMapping("/post-nota/{act_id}")
    public String postNote(
        @PathVariable("act_id") Integer act_id,
        @RequestParam("act-note") Integer actNote) throws Exception {

            appService.handlePostRequest(
                act_id,
                actNote
            );

            return "redirect:/";
        }
}
