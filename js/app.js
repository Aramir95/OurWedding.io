/* -----------------------------------------------
/* How to use? : Check the GitHub README
/* ----------------------------------------------- */

/* To load a config file (particles.json) you need to host this demo (MAMP/WAMP/local)... */
/*
particlesJS.load('particles-js', 'particles.json', function() {
  console.log('particles.js loaded - callback');
});
*/

/* Otherwise just put the config content (json): */



//configuración personalizada
var particlesConfig =  
{
  "particles": {
    "number": {
      "value": 280,
      "density": {
        "enable": true,
        "value_area": 700
      }
    },
    "color": {
      "value": ["#ff9000", "#ff0266", "#00ffff","#15ff00"]
    },
    "shape": {
      "type": "circle",
      "stroke": {
        "width": 0.5,
        "color": ["#ff9000", "#ff0266", "#00ffff"]
      },
      "polygon": {
        "nb_sides": 3
      },
      "image": {
        "src": "img/github.svg",
        "width": 100,
        "height": 100
      }
    },
    "opacity": {
      "value": 0.8,
      "random": false,
      "anim": {
        "enable": true,
        "speed": 1,
        "opacity_min": 0.5,
        "sync": false
      }
    },
    "size": {
      "value": 5,
      "random": true,
      "anim": {
        "enable": false,
        "speed": 40,
        "size_min": 0.1,
        "sync": false
      }
    },
    "line_linked": {
      "enable": true,
      "distance": 140,
      "color": "#e47a2e",
      "opacity": 0.4,
      "width": 1
    },
    "move": {
      "enable": true,
      "speed": 6,
      "direction": "none",
      "random": false,
      "straight": false,
      "out_mode": "out",
      "bounce": false,
      "attract": {
        "enable": false,
        "rotateX": 600,
        "rotateY": 1200
      }
    }
  },
  "interactivity": {
    "detect_on": "canvas",
    "events": {
      "onhover": {
        "enable": false,
        "mode": "bubble"
      },
      "onclick": {
        "enable": false,
        "mode": "repulse"
      },
      "resize": true
    },
    "modes": {
      "grab": {
        "distance": 200,
        "line_linked": {
          "opacity": 1
        }
      },
      "bubble": {
        "distance": 400,
        "size": 8,
        "duration": 2,
        "opacity": 8,
        "speed": 3
      },
      "repulse": {
        "distance": 200,
        "duration": 0.4
      },
      "push": {
        "particles_nb": 4
      },
      "remove": {
        "particles_nb": 2
      }
    }
  },
  "retina_detect": true
};

// Obtener el ancho de la pantalla
var screenWidth = window.innerWidth;

// Ajustar el número de partículas en función del ancho de la pantalla
if (screenWidth < 576) { // Pantallas más pequeñas que 576px
  particlesConfig.particles.number.value = 50;
  particlesConfig.particles.number.density.value_area=200;
}else if (screenWidth < 768) { // Pantallas más pequeñas que 768px
  particlesConfig.particles.number.value = 100;
} else if (screenWidth < 992) { // Pantallas entre 768px y 991px
  particlesConfig.particles.number.value = 200;
} else { // Pantallas más grandes que 991px
  particlesConfig.particles.number.value = 280;
};

particlesJS('particles-js',
 particlesConfig
);
