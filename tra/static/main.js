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
        placeholder: "Respond to the question",
      },
    ],
  ]);
}

function notificationHandler() {
    return {
        type: "is-success",
        text: "test",
        animated : false,
        timeout : 3000,
        async init() {
          await this.$nextTick();
        },
        async updateNoti(e) {
            this.type = e.detail.cat;
            this.text = e.detail.msg;
            this.animated = true;
            await new Promise(r => setTimeout(r, this.timeout));
            this.animated = false;
        }
    }
}

// creates a notification
function notify(msg, cat) {
  window.dispatchEvent(
        // notify what went wrong
        new CustomEvent('notify', 
        {
            detail : {
                msg : msg,
                cat : cat
                }   
            }
        )
  );
  console.log("Notify called")
}

// checks if the request is ok then converts to json
async function checkOk(res) {
    if (!res.ok) {
      res = await res.json()
      notify(res.error, "is-danger");
      throw Error("Something went wrong");
    }
    return await res.json() 
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
