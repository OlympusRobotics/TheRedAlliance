// enum for question types
class Enum {
  constructor(name) {
    this.name = name;
  }
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
}

class PropertyTypes extends Enum {
  static Prompt = new PropertyTypes("Prompt");
  static TextBox = new PropertyTypes("TextBox");
  // contains all the properties for each of the property types
  static templates = new Map([
    [
      PropertyTypes.Prompt.toString(),
      {
        text: "Question Prompt - Click to Edit",
      },
    ],
    [
      PropertyTypes.TextBox.toString(),
      {
        placeholder: "",
      },
    ],
  ]);
}

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
