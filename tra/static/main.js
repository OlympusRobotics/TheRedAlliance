// enum for question types
class Enum {
  constructor(name) {
    this.name = name;
  }
  /**
   * @param {Object} a - Object containing name property
   */
  equals(a) {
    return this.name === a.name;
  }
  toString() {
    return this.name;
  }
}

// question types are the overall type of question while PropertyType
// refers to the role the question component is actually playing
class QuestionTypes extends Enum {
  static TextBox = new QuestionTypes("TextBox");
  static MultipleChoice = new QuestionTypes("MultipleChoice");
  static ImageSelect = new QuestionTypes("ImageSelect");
  static NumInp = new QuestionTypes("NumInp");
  static LevelSelect = new QuestionTypes("LevelSelect");
}

class PropertyTypes extends Enum {
  static Prompt = new PropertyTypes("Prompt");
  static TextBox = new PropertyTypes("TextBox");
  static ImageSelect = new PropertyTypes("ImageSelect");
  static NumInp = new PropertyTypes("NumInp");
  static LevelSelect = new QuestionTypes("LevelSelect");
  // contains all the properties for each of the property types
  static templates = new Map([
    [
      PropertyTypes.Prompt.toString(),
      {
        text: "Click to Edit",
      },
    ],
    [
      PropertyTypes.TextBox.toString(),
      {
        placeholder: "Enter response",
      },
    ],
    [
      PropertyTypes.ImageSelect.toString(),
      {
        selected: [0, 0], // coordinates of the selected point
      },
    ],
    [
      PropertyTypes.NumInp.toString(),
      {
        max: 10,
        min: 0,
      },
    ],
    [
      PropertyTypes.LevelSelect.toString(),
      {
        levels: [],
      },
    ],
  ]);
}

function notificationHandler() {
  return {
    type: "is-success",
    text: "test",
    animated: false,
    async init() {
      await this.$nextTick();
    },
    async updateNoti(e) {
      this.type = e.detail.cat;
      this.text = e.detail.msg;
      this.animated = true;
      await new Promise((r) => setTimeout(r, e.detail.timeout));
      this.animated = false;
    },
  };
}

// creates a notification
function notify(msg, cat, timeout = 1500) {
  window.dispatchEvent(
    // notify what went wrong
    new CustomEvent("notify", {
      detail: {
        msg: msg,
        cat: cat,
        timeout: timeout,
      },
    })
  );
}

// checks if the request is ok then converts to json
async function checkOk(res) {
  if (!res.ok) {
    res = await res.json();
    notify(res.error, "is-danger");
    throw Error("Something went wrong");
  }
  return await res.json();
}

//--------- components
// the original dimensions of the field image
const FIELD_X = 773;
const FIELD_Y = 342;

const ImageSelect = () => ({
  img: null,
  // size used to scale coordinates
  size: null,
  // coords of image
  coords: {
    x: 0,
    y: 0,
  },
  init() {
    this.$watch("img", () => {
      if (this.img != null) {
        // when the img is loaded, get the width and height to scale te coord
        this.img.onload = async () => {
          // wait to allow img to load fully
          await new Promise((r) => setTimeout(r, 1000));
          this.coords = getPos(this.img);
          this.size = {
            x: this.img.width,
            y: this.img.height,
          };
        };
      }
    });
  },
  scaleCoords(point) {
    var scaled = {
      x: (this.size.x / FIELD_X) * point[0] + this.coords.x,
      y: (this.size.y / FIELD_Y) * point[1] + this.coords.y,
    };
    return scaled;
  },
});

// uses in form.html only
const ImageSelectPublic = (index) => ({
  img: null,
  size: null,
  dot: {
    x: 0,
    y: 0,
  },
  // coords of image
  coords: {
    x: 0,
    y: 0,
  },
  init() {
    this.$watch("img", () => {
      if (this.img != null) {
        // when the img is loaded, get the width and height to scale te coord
        this.img.onload = async () => {
          this.coords = getPos(this.img);
          this.size = {
            x: this.img.width,
            y: this.img.height,
          };
        };
      }
    });
  },
  setDot(e) {
    // get pos relative to 0,0 on the image
    this.dot.x = parseInt(e.pageX - this.coords.x - 4);
    this.dot.y = parseInt(e.pageY - this.coords.y - 4);
    var scaled = this.scaleCoords(this.dot);
    this.$store.responses[index] = [scaled.x, scaled.y];
  },
  // scales up to original size
  scaleCoords(dot) {
    return {
      x: parseInt((FIELD_X / this.size.x) * dot.x),
      y: parseInt((FIELD_Y / this.size.y) * dot.y),
    };
  },
});
const getPos = (el) => {
  const rect = el.getBoundingClientRect();
  return {
    x: window.scrollX + rect.left,
    y: window.scrollY + rect.top,
  };
};

const LevelSelectRes = (index) => ({
  levels: [0, 0, 0],
  init() {},
  getAverages(responses) {
    if (responses === undefined) 
      return;

    responses.forEach((e) => {
      for (let i = 0; i<e.responses[index].length; i++) {
        this.levels[i] += e.responses[index][i];
      }
    });
      
    this.levels = this.levels.map((e) => e / responses.length);
  },
});

const LevelSelect = (index) => ({
  levels: [0, 0, 0],
  init() {
    this.$store.responses[index] = this.levels;
  },
  increment(level, x) {
    if (this.levels[level] + x >= 0 && this.levels[level] + x <= 30) {
      this.levels[level] += x;
    }
    this.$store.responses[index] = this.levels;
  },
});

const NumInp = (min, max, index) => ({
  val: min,
  min: min,
  max: max,
  init() {
    this.$store.responses[index] = this.val;
    this.$watch("val", () => {
      this.validate();
      this.$store.responses[index] = this.val;
    });
  },
  validate() {
    // make sure not to pass
    if (parseInt(this.val) > this.max) {
      this.val = this.max;
    }
    if (parseInt(this.val) < this.min) {
      this.val = this.min;
    }
  },
});

// loads the img into a data url so that it can be used in offline mode

const getFieldImage = async () => {
  if (this.fieldImg) {
    return this.fieldImg;
  }
  this.fieldImg = loadImg("/static/assets/field.jpg");
  return this.fieldImg;
};

const getDefaultPfp = async () => {
  if (this.pfp) {
    return this.pfp;
  }
  this.pfp = loadImg("/static/assets/robot-cat.png");
  return this.pfp;
};

const loadImg = async (url) => {
  // get the img
  var blob = await fetch(url).then((r) => r.blob());
  return await new Promise((resolve) => {
    // read it as a data url
    let reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.readAsDataURL(blob);
  });
};

// ---------- Straight from Bulma website https://bulma.io/documentation/components/navbar/
// controls the navbar burger
document.addEventListener("DOMContentLoaded", () => {
  // Get all "navbar-burger" elements
  const $navbarBurgers = Array.prototype.slice.call(
    document.querySelectorAll(".navbar-burger"),
    0
  );

  // Add a click event on each of them
  $navbarBurgers.forEach((el) => {
    el.addEventListener("click", () => {
      // Get the target from the "data-target" attribute
      const target = "main-menu";
      const $target = document.getElementById(target);

      // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
      el.classList.toggle("is-active");
      $target.classList.toggle("is-active");
    });
  });
});
