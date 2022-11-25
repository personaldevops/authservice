from appservicecore.api_service import APIService, APIServiceRequest

if __name__ == "__main__":
    service_request = APIServiceRequest()
    service_request.name('app.authservice')
    service_request.port(7171)
    service_request.add_packages('authservice.api')
    service_request.add_packages('authservice.models')
    APIService(request=service_request).start()
