# Networking Integration

**Last Updated:** October 14, 2025  
**Status:** ✅ Complete

---

## Setup

```yaml
dependencies:
  dio: ^5.4.0
```

---

## API Client

```dart
import 'package:dio/dio.dart';

class ApiClient {
  static final Dio _dio = Dio(
    BaseOptions(
      baseUrl: Environment.apiBaseUrl,
      connectTimeout: Duration(seconds: 5),
      receiveTimeout: Duration(seconds: 3),
    ),
  );
  
  static void init() {
    _dio.interceptors.add(LogInterceptor());
    _dio.interceptors.add(AuthInterceptor());
  }
  
  static Future<Response> get(String path) async {
    return await _dio.get(path);
  }
  
  static Future<Response> post(String path, dynamic data) async {
    return await _dio.post(path, data: data);
  }
}
```

---

## Auth Interceptor

```dart
class AuthInterceptor extends Interceptor {
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    final token = StorageService.getSetting<String>('auth_token');
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    handler.next(options);
  }
  
  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    if (err.response?.statusCode == 401) {
      // Handle token refresh
    }
    handler.next(err);
  }
}
```

---

**Status:** ✅ Networking Integration Complete

