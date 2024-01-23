BUSSO ALEJO - API TEST Mo Credit

El challenge esta resuelto en su totalidad, con los puntos adicionales requeridos.
El entorno esta Dockerizado.

Para levantar el entorno:
  - git clone https://github.com/alejo0998/BussoAlejoChallengeMOCredit
  - git checkout master
  - docker-compose up // Puede requerir permisos de sudo.

Una vez realizado esto el entorno ya deberia estar funcionando, se ejecutara primero las migraciones, luego los test automatizados y ya deberia quedar el entorno levantado
para acceder desde http://localhost:8000/

Para probar la API, se agrego swagger, utilizando django-spectacular, en http://localhost:8000/api/schema/swagger-ui/ , se encuentra la interfaz grafica para poder
probar los endpoints, importante destacar que antes de usar cualquier endpoint hay que hacer un request POST a /api/key/ para obtener el ApiKey necesario, una vez obtenido el apiKey agregarlo en la autenticacion del swagger-ui, donde va con el formato Api-Key <key>. En caso de usar el swagger-ui, caso de utilizarlo por postman se debe agregar el encabezado en un header de Authorization, tambien con el mismo formato.
Respecto al apiKey, unicamente cree el endpoint para que devuelva un token, sin solicitar usuario ni password porque considere que no lo ameritaba para el challenge y agregaria una complejidad extra de crear usuarios cuando no era lo solicitado.
En http://localhost:8000/api/schema/redoc/ se encuentra la documentacion de la api.

Customers:
-  Para la creacion de customers via un archivo plano, agregue en formato csv un ejemplo de como deberia agregar los diferentes customers y se crea con el comando load_customers el cual pide como parametro la ubicacion de donde esta el archivo csv para leerlo y crear los objetos indicados.

Modelado:
-  Respecto al modelo, respete lo indicado en el DER, con una unica modificacion donde agregue un motivo de rechazo en el modelo Payments, para caso de que se rechace un pago quede persistido el porque.
-  Se setearon los correspondientes defaults en el modelo.
-  Respete como primary key el id y como unique el external_id, entiendo la utilidad de tener como primary_key un id, y que por razones de seguridad en los endpoints se acceda mediante el external_id.

Test:
- Se agregaron los test de la mayoria de los casos mas relevantes, unicamente con unittest, se corren los test con python manage.py test , en otros casos utilice herramientas para a su vez ver el coverage del test y ver que casos estan cubiertos.

Endpoints:
- Los endpoints se encuentran todos los solicitados, incluyendo lo extra, la gran mayoria son post y gets, exceptuando el del modelo loans que tiene un put para actualizar el status del prestamo y asi poder realizar los pagos sobre el mismo.
- El endpoint con mas logica es el endpoint de la realizacion de los pagos, en este caso todo lo que es las validaciones las realice en el serializer, y la creacion del modelo con su manytomany al detalle de los pagos. En este endpoint se debe enviar el customer_external_id, el nuevo external_id del nuevo payment, y el detalle de los pagos que se realizan, de que prestamo es y el monto por cada prestamo que se va a pagar. En el lado del servidor se hacen las validaciones, si la validacion rompe por algun motivo se crea igualmente el pago con estado rechazado y los pagos no impactan, es decir no se modifica el modelo loan. En caso de que las validaciones pasen, se crea el pago con estado aceptado y los pagos correspondientes impactan en el modelo loan y se hacen las actualizaciones pertinentes. Tambien la cuestion del monto del pago no la estoy enviando en el endpoint y la calculo como la suma de todos los pagos que voy a realizar por cada loan.

