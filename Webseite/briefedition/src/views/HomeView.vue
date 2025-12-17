<template>
  <div class="home">

    <div class="row justify-content-center align-items-center">

      <!-- Bild von Sophie von La Roche -->
      <div class="col-sm-3 text-center">
        <img src="/img/LaRoche_Portrait.jpg" class="portrait">
      </div>

      <!-- Zitate-Carousel -->
      <div class="col-sm-4 text-center">


        <div id="carouselText" class="carousel slide" data-bs-ride="carousel" data-bs-interval="8000">
          <!-- Indicators -->
          <div class="carousel-indicators">
            <button type="button" data-bs-target="#carouselText" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
            <button type="button" data-bs-target="#carouselText" data-bs-slide-to="1" aria-label="Slide 2"></button>
            <button type="button" data-bs-target="#carouselText" data-bs-slide-to="2" aria-label="Slide 3"></button>
          </div>
          <div class="carousel-inner text-center">
            <div class="carousel-item active">
              <div class="d-flex justify-content-center align-items-center" style="height: 250px;">
                <div>
                  <p>&bdquo;O wie danke ich Gott und Ihnen das Sie hier waren - kommen Sie - O kommen Sie Zu mir - ich will Sie wie einen zweyten Frantz empfangen und stetts so für Sie denken&ldquo;</p>
                </div>
              </div>
            </div>
            <div class="carousel-item">
              <div class="d-flex justify-content-center align-items-center" style="height: 250px;">
                <div>
                  <p>&bdquo;Klopstok ist für mich, was kant unter den Philosophen – Wieland aber ist reines Licht, wo alles sichtbar, u wo nichts blendet&ldquo;</p>
                </div>
              </div>
            </div>
            <div class="carousel-item">
              <div class="d-flex justify-content-center align-items-center" style="height: 250px;">
                <div>
                  <p>&bdquo;O mein Freund! was ist für eine zerstörende Moralische Lava, aus der revolution von Paris außgeströmt&ldquo;</p>
                </div>
              </div>
            </div>

          </div> <!-- Carousel schließen -->
        </div>
        <!-- Button zu den Briefen-->
        <a class="btn btn-dark btn-lg button" href="/briefe" role="button">→ Zu den Briefen</a>
      </div> <!-- col schließen -->
    
      <!-- Bild von Johann Isaak von Gerning -->
      <div class="col-sm-3 text-center">
        <img src="/img/Gerning_Portrait.jpg" class="portrait">
      </div>

    </div> <!-- row schließen-->
  </div>
</template>

<script>
export default {
  name: "HomeView",
};
</script>

<style scoped>

.carousel-inner {
  min-height: 250px;
  background-color: bisque;
  align-items: center; /* vertikal zentrieren */
  justify-content: center; /* horizontal zentrieren */
}


.carousel-inner p {
  font-size: 20px;
  font-style: italic;
  font-family:'Courier New', Courier, monospace;
  font-weight: bold;
}

.carousel-item h3,
.carousel-item p {
  margin: 0;
}

/* Blaue Carousel-Indikatoren */
.carousel-indicators button {
  background-color: gray !important; /* inaktive Punkte */
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.carousel-indicators .active {
  background-color: #020664 !important; /* aktiver Punkt */
  width: 14px;
  height: 14px;
  border-radius: 50%;
}



/* Portrait-Bilder */
.portrait {
  width: 240px;       /* Breite anpassen */
  height: 320px;      /* Höhe anpassen */
  object-fit: cover;  /* Bild zuschneiden, ohne zu verzerren */
  border-radius: 50%; /* Oval/Rund */
  display: block;
  margin: 0 auto;     /* zentrieren */
  border: 5px solid #020664; /* blauer Rahmen */
}

.row.justify-content-center.align-items-center {
  margin-top: 20px;
}

.button {
  background-color: #020664 !important;
  margin-top: 20px;
}



</style>
