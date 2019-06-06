import http.server
import socketserver

# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 8000


# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        path=self.path 
        if path==("/"):
            with open("index.html","r") as file:
                content=file.read()
            message = str(content)
            self.wfile.write(bytes(message, "utf8"))
            print("File served!")
		
        elif path.startswith("/searchDrug"):
            contenido=path.lstrip('/searchDrug?active_ingredient')

            try:
                if contenido.count("&")==1:
                    contenido=contenido.split("&")
                    nombre=str(contenido[0])
                    nombre=nombre.lower()
                    nombre=nombre.replace("=","")
                    limit=str(contenido[1])
                    limit=limit.strip("Limit=")
                elif contenido.count("?")==1:
                    contenido=contenido.split("?")
                    nombre=str(contenido[0])
                    nombre=nombre.lower()
                    nombre=nombre.replace("=","")
                    limit=str(contenido[1])
                    limit=limit.strip("Limit=")
                else:
                    limit=str(10)
                    nombre=contenido.lower()
                    nombre=nombre.replace("=","")
            
            
            except IndexError or IndentationError:
                limit=str(10)
                nombre=contenido.lower()
                nombre=nombre.replace("=","")
            
            try:
                if limit=="":
                    limit=str(10)
            except TypeError:
                limit=str(10)
            
            import requests

            url=str("https://api.fda.gov/drug/label.json?search=active_ingredient:"+nombre+"&limit="+limit)
            data=requests.get(url).json()
            

            lista_genericos=[]
            try:
                for result in data['results']:
                    try: 
                        comun=result['openfda']
                        generico=comun['generic_name']
                        lista_genericos+=["<li>"+str(generico)]
                    except KeyError:
                        lista_genericos+=["<li>Medicamento sin nombre generico"]
                content=(str(lista_genericos)).replace("[","")
                content=content.replace("]","")
                content=content.replace("'","")
                content=content.replace('"',"")
                content=content.replace(',',"")
                message=str("<b>LISTA DE MEDICAMENTOS</b><br>"+content)
            except KeyError:
                message=("<b>ERROR</b><br>Nombre de medicamento no valido")
                
            

            
        # Write content as utf-8 data
            self.wfile.write(bytes(message, "utf8"))
            
			
        elif path.startswith("/searchCompany?company"):
            contenido=path.lstrip('/searchCompany?company')
            try:
                if contenido.count("&")==1:
                    contenido=contenido.split("&")
                    nombre=str(contenido[0])
                    nombre=nombre.lower()
                    nombre=nombre.replace("=","")
                    limit=str(contenido[1])
                    limit=limit.strip("Limit=")
                elif contenido.count("?")==1:
                    contenido=contenido.split("?")
                    nombre=str(contenido[0])
                    nombre=nombre.lower()
                    nombre=nombre.replace("=","")
                    limit=str(contenido[1])
                    limit=limit.strip("Limit=")
                else:
                    limit=str(10)
                    nombre=contenido.lower()
                    nombre=nombre.replace("=","")
            
            
            except IndexError or IndentationError:
                limit=str(10)
                nombre=contenido.lower()
                nombre=nombre.replace("=","")
            
            try:
                if limit=="":
                    limit=str(10)
            except TypeError:
                limit=str(10)
         
            import requests

            url=str("https://api.fda.gov/drug/label.json?search=openfda.manufacturer_name:"+nombre+"&limit="+limit)
            data=requests.get(url).json()

            lista_comp=[]
            for result in data['results']:
                try: 
                    comun=result['openfda']
                    comp=comun['manufacturer_name']
                    lista_comp+=["<li>"+str(comp)]
                except KeyError:
                    lista_comp+=["<li>Medicamento sin marca"]

            content=(str(lista_comp)).replace("[","")
            content=content.replace("]","")
            content=content.replace("'","")
            content=content.replace('"',"")
            content=content.replace(',',"")
            

            message=str("LISTA DE COMPANYS<br>"+content)
        # Write content as utf-8 data
            self.wfile.write(bytes(message, "utf8"))
            
        elif path.startswith("/listDrugs"):
            limit=path.strip("/listDrugs?Limit=")
            try:
                if limit=="":
                    limit=str(10)
            except TypeError:
                limit=str(10)
            import requests
            url=str("https://api.fda.gov/drug/ndc.json?count=generic_name.exact&limit="+limit)
            data=requests.get(url).json()
            lista_gen=[]
            for result in data['results']:
                try: 
                    gen=result['term']
                    lista_gen+=["<li>"+str(gen)]
                except KeyError:  
                    lista_gen+=["<li>Medicamento sin nombre generico"]
            content=(str(lista_gen)).replace("[","")
            content=content.replace("]","")
            content=content.replace("'","")
            content=content.replace('"',"")
            content=content.replace(',',"")

            message=str("LISTA DE MEDICAMENTOS<br>"+content)

            self.wfile.write(bytes(message, "utf8"))
			
        elif path.startswith("/listCompanies"):
            limit=path.strip("/listCompanies?Limit=")
            
            try:
                if limit=="":
                    limit=str(10)
            except TypeError:
                limit=str(10)
            import requests
            url=str("https://api.fda.gov/drug/ndc.json?count=openfda.manufacturer_name.exact&limit="+limit)
            data=requests.get(url).json()
            lista_comp=[]
            for result in data['results']:
                try: 
                    comp=result['term']
                    lista_comp+=["<li>"+str(comp)]
                except KeyError:  
                    lista_comp+=["<li>Medicamento sin ,marca"]
            content=(str(lista_comp)).replace("[","")
            content=content.replace("]","")
            content=content.replace("'","")
            content=content.replace('"',"")
            content=content.replace(',',"")
            

            message=str("LISTA DE COMPANYS<br>"+content)

            self.wfile.write(bytes(message, "utf8"))

        elif path.startswith("/listWarnings"):

            limit=path.lstrip("/listWarnings?Limit=")
			
            try:
                if limit=="":
                    limit=str(10)
            except TypeError:
                limit=str(10)
            
            
            import requests
            url=str("https://api.fda.gov/drug/label.json?search=warnings&limit="+limit)
            
            data=requests.get(url).json()
            lista_war=[]
            for result in data['results']:
                try: 
                    war=result['warnings']
                    lista_war+=["<li>"+str(war)]
                except KeyError:
                    lista_war+=["<li>Medicamento sin advertencia"]
					
            content=(str(lista_war)).replace("[","")
            content=content.replace("]","")
            content=content.replace("'","")
            content=content.replace('"',"")
            
            

            message=str("LISTA DE ADVERTENCIAS<br>"+content)
            self.wfile.write(bytes(message, "utf8"))
        else:
            message=("<b>ERROR 404</b><br>El recurso solicitado no existe. Revise el path.")
            self.wfile.write(bytes(message, "utf8"))
        
            
            

            
            
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer((IP, PORT), Handler)

print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
        pass

httpd.server_close()
print("")
print("Server stopped!")
