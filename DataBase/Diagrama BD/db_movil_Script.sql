
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema bd_movil
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `bd_movil` DEFAULT CHARACTER SET utf8mb4 ;
USE `bd_movil` ;

-- -----------------------------------------------------
-- Table `bd_movil`.`Usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd_movil`.`Usuario` (
  `UserID` INT NOT NULL AUTO_INCREMENT,
  `Nombre` VARCHAR(255) NULL DEFAULT NULL,
  `Direccion` VARCHAR(255) NULL DEFAULT NULL,
  `Email` VARCHAR(255) NULL DEFAULT NULL,
  `Telefono` VARCHAR(15) NULL DEFAULT NULL,
  `Codigo` VARCHAR(10) NULL,
  `Verificacion` VARCHAR(3) NULL DEFAULT 'NO',
  PRIMARY KEY (`UserID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `bd_movil`.`Tienda`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd_movil`.`Tienda` (
  `TiendaID` INT NOT NULL AUTO_INCREMENT,
  `Nombre` VARCHAR(255) NULL DEFAULT NULL,
  `Descripcion` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`TiendaID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `bd_movil`.`Pedido`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd_movil`.`Pedido` (
  `PedidoID` INT NOT NULL AUTO_INCREMENT,
  `UserID` INT NULL DEFAULT NULL,
  `TiendaID` INT NULL DEFAULT NULL,
  `PrecioTotal` DECIMAL(10,2) NULL DEFAULT NULL,
  `FechaPedido` VARCHAR(30) NULL DEFAULT NULL,
  `Estado` VARCHAR(20) NULL DEFAULT NULL,
  `Direccion` VARCHAR(400) NULL,
  PRIMARY KEY (`PedidoID`),
  INDEX `UserID` (`UserID` ASC) VISIBLE,
  INDEX `TiendaID` (`TiendaID` ASC) VISIBLE,
  CONSTRAINT `pedidos_ibfk_1`
    FOREIGN KEY (`UserID`)
    REFERENCES `bd_movil`.`Usuario` (`UserID`),
  CONSTRAINT `pedidos_ibfk_2`
    FOREIGN KEY (`TiendaID`)
    REFERENCES `bd_movil`.`Tienda` (`TiendaID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `bd_movil`.`Producto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd_movil`.`Producto` (
  `ProductoID` INT NOT NULL AUTO_INCREMENT,
  `TiendaID` INT NULL DEFAULT NULL,
  `Nombre` VARCHAR(255) NULL DEFAULT NULL,
  `Descripcion` TEXT NULL DEFAULT NULL,
  `Precio` DECIMAL(10,2) NULL DEFAULT NULL,
  PRIMARY KEY (`ProductoID`),
  INDEX `TiendaID` (`TiendaID` ASC) VISIBLE,
  CONSTRAINT `productos_ibfk_1`
    FOREIGN KEY (`TiendaID`)
    REFERENCES `bd_movil`.`Tienda` (`TiendaID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `bd_movil`.`DetallesPedido`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd_movil`.`DetallesPedido` (
  `DetalleID` INT NOT NULL AUTO_INCREMENT,
  `PedidoID` INT NULL DEFAULT NULL,
  `ProductoID` INT NULL DEFAULT NULL,
  `Cantidad` INT NULL DEFAULT NULL,
  `PrecioUnitario` DECIMAL(10,2) NULL DEFAULT NULL,
  PRIMARY KEY (`DetalleID`),
  INDEX `PedidoID` (`PedidoID` ASC) VISIBLE,
  INDEX `ProductoID` (`ProductoID` ASC) VISIBLE,
  CONSTRAINT `detallespedido_ibfk_1`
    FOREIGN KEY (`PedidoID`)
    REFERENCES `bd_movil`.`Pedido` (`PedidoID`),
  CONSTRAINT `detallespedido_ibfk_2`
    FOREIGN KEY (`ProductoID`)
    REFERENCES `bd_movil`.`Producto` (`ProductoID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;



-- Insertar datos de tienda
INSERT INTO `bd_movil`.`Tienda` (`TiendaID`, `Nombre`, `Descripcion`) 
VALUES 
(1, 'Food Truck Delicias', 'Ofrecemos una variedad de delicias culinarias sobre ruedas.'),
(2, 'Sabores Exquisitos Móviles', 'Descubre sabores exquisitos en nuestro food truck.'),
(3, 'Ruedas de Sabor', 'Explora el mundo de los sabores en cada plato.'),
(4, 'Comida sobre Ruedas Express', 'La mejor comida rápida en tu lugar favorito.'),
(5, 'Gastronomía Móvil Gourmet', 'Experimenta la alta cocina en un ambiente informal.');


-- Insertar datos de productos (comida) para la Tienda 1
INSERT INTO `bd_movil`.`Producto` (`TiendaID`, `Nombre`, `Descripcion`, `Precio`) 
VALUES 
(1, 'Hamburguesa Clásica', 'Carne de res, queso, lechuga y tomate', 179.19),
(1, 'Wrap de Pollo', 'Tortilla de trigo rellena de pollo, verduras frescas y salsa especial', 150.75),
(1, 'Papas Fritas Gourmet', 'Papas fritas crujientes con condimentos gourmet', 99.90),
(1, 'Ensalada de la Casa', 'Ensalada fresca con mezcla de hojas, tomate y aderezo casero', 139.29),
(1, 'Batido de Frutas', 'Batido refrescante con mezcla de frutas de la temporada', 79.92);

-- Insertar datos de productos (comida) para la Tienda 2
INSERT INTO `bd_movil`.`Producto` (`TiendaID`, `Nombre`, `Descripcion`, `Precio`) 
VALUES 
(2, 'Tacos de Pollo al Pastor', 'Tortillas de maíz con pollo marinado al pastor y piña', 213.75),
(2, 'Burrito Vegetariano', 'Burrito relleno de frijoles, arroz, verduras y guacamole', 179.19),
(2, 'Nachos Supreme', 'Nachos cubiertos con queso derretido, carne, guacamole y crema', 215.89),
(2, 'Margarita de Frutas', 'Cóctel refrescante con mezcla de frutas y tequila', 143.91),
(2, 'Churros con Chocolate', 'Churros crujientes acompañados de salsa de chocolate caliente', 96.36);

-- Insertar datos de productos (comida) para la Tienda 3
INSERT INTO `bd_movil`.`Producto` (`TiendaID`, `Nombre`, `Descripcion`, `Precio`) 
VALUES 
(3, 'Pizza Pepperoni', 'Pizza con salsa de tomate, queso mozzarella y rodajas de pepperoni', 227.89),
(3, 'Calzone de Jamón y Queso', 'Masa rellena de jamón, queso y salsa de tomate', 199.58),
(3, 'Lasagna Casera', 'Lasaña con capas de pasta, carne, queso y salsa de tomate', 243.74),
(3, 'Cannoli Siciliano', 'Postre italiano relleno de crema de ricotta y chocolate', 139.29),
(3, 'Granita de Limón', 'Postre siciliano a base de hielo y jugo de limón', 89.01);

-- Insertar datos de productos (comida) para la Tienda 4
INSERT INTO `bd_movil`.`Producto` (`TiendaID`, `Nombre`, `Descripcion`, `Precio`) 
VALUES 
(4, 'Hot Dog con Chili', 'Hot dog con salchicha, chili con carne y queso cheddar', 139.29),
(4, 'Chicken Nuggets', 'Nuggets de pollo crujientes con salsa de mostaza y miel', 110.00),
(4, 'Poutine de Camarones', 'Papas fritas con queso y camarones bañados en salsa gravy', 199.90),
(4, 'Batido de Oreos', 'Batido cremoso con galletas Oreo trituradas', 99.90),
(4, 'Té Helado de Durazno', 'Té helado refrescante con sabor a durazno', 69.41);

-- Insertar datos de productos (comida) para la Tienda 5
INSERT INTO `bd_movil`.`Producto` (`TiendaID`, `Nombre`, `Descripcion`, `Precio`) 
VALUES 
(5, 'Sushi Roll Tempura', 'Roll de sushi con tempura, aguacate y salsa teriyaki', 374.85),
(5, 'Sashimi de Salmón', 'Finas láminas de salmón fresco cortadas a mano', 412.50),
(5, 'Edamame Trufado', 'Vainas de soja al vapor con aceite de trufa y sal', 205.11),
(5, 'Miso Ramen', 'Sopa de fideos ramen con miso, huevo y vegetales', 347.92),
(5, 'Mochi de Mango', 'Postre japonés de arroz glutinoso relleno de mango', 149.33);
