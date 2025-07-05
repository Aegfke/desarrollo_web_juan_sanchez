package tarea4.tarea4.models;

import java.time.LocalDateTime;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.SequenceGenerator;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;

@Entity
@Table(name="actividad")
public class Activity {

    @Id
    @SequenceGenerator(
        name = "act_sequence",
        sequenceName = "act_sequence",
        allocationSize = 1
    )
    @GeneratedValue(
        strategy = GenerationType.SEQUENCE,
        generator = "act_sequence"
    )
    private Integer id;

    @NotNull
    private Integer comunaId;

    private String sector;

    @NotNull
    private String nombre;

    @NotNull
    private String email;

    private String celular;

    @NotNull
    private LocalDateTime dia_hora_inicio;

    private LocalDateTime dia_hora_termino;

    public Activity() {
    }
    
    public Integer getId() {
        return id;
    }
    public Integer getComunaId() {
    return comunaId;
    }

    public String getSector() {
        return sector;
    }

    public String getNombre() {
        return nombre;
    }

    public String getEmail() {
        return email;
    }

    public String getCelular() {
        return celular;
    }

    public LocalDateTime getHoraInicio() {
        return dia_hora_inicio;
    }

    public LocalDateTime getHoraTermino() {
        return dia_hora_termino;
    }
}
