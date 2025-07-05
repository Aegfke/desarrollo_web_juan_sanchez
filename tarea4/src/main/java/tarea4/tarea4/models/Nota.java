package tarea4.tarea4.models;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.SequenceGenerator;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;


@Entity
@Table(name="nota")
public class Nota {

    @Id
    @SequenceGenerator(
        name = "nota_sequence",
        sequenceName = "nota_sequence",
        allocationSize = 1
    )
    @GeneratedValue(
        strategy = GenerationType.SEQUENCE,
        generator = "nota_sequence"
    )
    private Integer id;

    @NotNull
    private Integer actividadId;

    @NotNull
    private Integer nota;

    public Nota() {
    }

    public Nota(Integer actividadId,
                Integer nota) {
        this.actividadId = actividadId;
        this.nota = nota;
    }

    public Integer getId() {
        return id;
    }

    public Integer getActividadId() {
        return actividadId;
    }

    public Integer getNota() {
        return nota;
    }

    public static Boolean validateNota(Integer nota) {
        return ((nota <= 7) && (nota >= 1));
    }

}