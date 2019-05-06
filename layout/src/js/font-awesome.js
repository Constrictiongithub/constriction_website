import { library, dom } from "@fortawesome/fontawesome-svg-core";
import { faSync } from "@fortawesome/free-solid-svg-icons/faSync";
import { faHome } from "@fortawesome/free-solid-svg-icons/faHome";
import { faTruck } from "@fortawesome/free-solid-svg-icons/faTruck";
import { faSuitcase } from "@fortawesome/free-solid-svg-icons/faSuitcase";
import { faBuilding } from "@fortawesome/free-solid-svg-icons/faBuilding";
import { faUsers } from "@fortawesome/free-solid-svg-icons/faUsers";
import { faGlobe } from "@fortawesome/free-solid-svg-icons/faGlobe";
import { faCog } from "@fortawesome/free-solid-svg-icons/faCog";
import { faLightbulb } from "@fortawesome/free-solid-svg-icons/faLightbulb";
import { faAngleRight } from "@fortawesome/free-solid-svg-icons/faAngleRight";
import { faAngleDown } from "@fortawesome/free-solid-svg-icons/faAngleDown";

library.add(
  faSync,
  faHome,
  faTruck,
  faSuitcase,
  faBuilding,
  faUsers,
  faGlobe,
  faCog,
  faLightbulb,
  faAngleRight,
  faAngleDown
);
dom.watch();
