from appservicecore.api_service import APIService, APIServiceRequest

if __name__ == "__main__":
    service_request = APIServiceRequest()
    service_request.name('app.api_service')
    service_request.port(7171)
    service_request.add_packages('authservice.api')
    APIService(request=service_request).start()
