package tarea4.tarea4.models;

import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.SequenceGenerator;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;

@Entity
@Table(name="actividad_tema")
public class Tema {

    @Id
    @SequenceGenerator(
        name = "tema_sequence",
        sequenceName = "tema_sequence",
        allocationSize = 1
    )
    @GeneratedValue(
        strategy = GenerationType.SEQUENCE,
        generator = "tema_sequence"
    )
    private Integer id;

    @Enumerated(EnumType.STRING)
    private TemaEnum tema;

    private String glosa_otro;

    @NotNull
    private Integer actividadId;


    public Integer getId() {
        return id;
    }

    public TemaEnum getTema() {
        return tema;
    }

    public String getGlosa_otro() {
        return glosa_otro;
    }

    public Integer getActividadId() {
        return actividadId;
    }
    
}
