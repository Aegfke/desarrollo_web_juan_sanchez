let obtenerNota = (list, act_id) => {
  if (!list || list.length == 0) {
    document.getElementById(`actividad-id-${act_id}`).textContent = "-";
    return;
  }
  
  let total = list.reduce((acc, nota) => acc + nota.nota, 0);
  let promedio = total / list.length;
  let promedioRedondeado = Math.round(promedio * 10) / 10;

  document.getElementById(`actividad-id-${act_id}`).textContent = `${promedioRedondeado}`;
}

let fetchAJAX = (url,act_id) => {
    fetch(url, {
        mode: "cors",
        credentials: "include",
    }) //url
      .then((response) => {
        if(!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((ajaxResponse) => {
        obtenerNota(ajaxResponse["data"], act_id);
      })
      .catch((error) => {
        console.error(
            "There has been a problem with your fetch operation",
            error
        );
      });
};

window.onload = () => {
  const filas = document.querySelectorAll("tr[data-actividad-id]");

   filas.forEach(fila => {
        const actividad_id = fila.getAttribute("data-actividad-id");
        fetchAJAX(`${window.origin}/get-activity-note/${actividad_id}`, actividad_id);
   });
};