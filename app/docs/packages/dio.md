# Dio - HTTP Client

**Current Project Version**: ^5.4.3+1  
**Latest Available Version**: ^5.4.3+1  
**Recommendation**: ✅ UP TO DATE

---

## Overview

Dio is a powerful HTTP client for Dart with support for interceptors, global configuration, FormData, request cancellation, file downloading, timeout, and more.

## Key Features

- **Interceptors**: Request/Response/Error interceptors
- **Global Configuration**: Base URL, headers, timeout
- **FormData**: Multipart form data support
- **Cancellation**: Cancel requests with tokens
- **Timeout**: Request, send, receive timeouts
- **Retry**: Built-in retry logic
- **Transformers**: Custom request/response transformers
- **Adapters**: HTTP/2, browsers, native

## Installation

```yaml
dependencies:
  dio: ^5.4.3+1
```

## Basic Usage

### Create Dio Instance

```dart
import 'package:dio/dio.dart';

final dio = Dio(
  BaseOptions(
    baseUrl: 'https://api.example.com',
    connectTimeout: Duration(seconds: 5),
    receiveTimeout: Duration(seconds: 3),
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
  ),
);
```

### GET Request

```dart
try {
  final response = await dio.get('/users');
  print(response.data);
} on DioException catch (e) {
  if (e.response != null) {
    print('Error: ${e.response?.statusCode}');
  } else {
    print('Error: ${e.message}');
  }
}
```

### POST Request

```dart
final response = await dio.post(
  '/users',
  data: {
    'name': 'John',
    'email': 'john@example.com',
  },
);
```

### Query Parameters

```dart
final response = await dio.get(
  '/users',
  queryParameters: {
    'page': 1,
    'limit': 10,
  },
);
```

## Interceptors

### Request Interceptor

```dart
dio.interceptors.add(
  InterceptorsWrapper(
    onRequest: (options, handler) {
      // Add auth token
      options.headers['Authorization'] = 'Bearer $token';
      return handler.next(options);
    },
    onResponse: (response, handler) {
      // Transform response
      return handler.next(response);
    },
    onError: (error, handler) {
      // Handle errors
      if (error.response?.statusCode == 401) {
        // Refresh token logic
      }
      return handler.next(error);
    },
  ),
);
```

### Logging Interceptor

```dart
dio.interceptors.add(
  LogInterceptor(
    request: true,
    requestHeader: true,
    requestBody: true,
    responseHeader: true,
    responseBody: true,
    error: true,
  ),
);
```

## Advanced Features

### File Upload

```dart
final formData = FormData.fromMap({
  'file': await MultipartFile.fromFile(
    './avatar.png',
    filename: 'avatar.png',
  ),
  'name': 'John',
});

await dio.post('/upload', data: formData);
```

### File Download

```dart
await dio.download(
  'https://example.com/file.pdf',
  './downloads/file.pdf',
  onReceiveProgress: (received, total) {
    if (total != -1) {
      print('${(received / total * 100).toStringAsFixed(0)}%');
    }
  },
);
```

### Request Cancellation

```dart
final cancelToken = CancelToken();

// Start request
dio.get('/users', cancelToken: cancelToken);

// Cancel request
cancelToken.cancel('Request cancelled');
```

### Retry Logic

```dart
import 'package:dio/dio.dart';

class RetryInterceptor extends Interceptor {
  final int maxRetries;
  final Duration retryDelay;

  RetryInterceptor({
    this.maxRetries = 3,
    this.retryDelay = const Duration(seconds: 1),
  });

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    if (err.requestOptions.extra.containsKey('retryCount')) {
      final retryCount = err.requestOptions.extra['retryCount'] as int;
      
      if (retryCount < maxRetries) {
        err.requestOptions.extra['retryCount'] = retryCount + 1;
        await Future.delayed(retryDelay);
        
        try {
          final response = await Dio().fetch(err.requestOptions);
          return handler.resolve(response);
        } catch (e) {
          return handler.next(err);
        }
      }
    } else {
      err.requestOptions.extra['retryCount'] = 1;
      await Future.delayed(retryDelay);
      
      try {
        final response = await Dio().fetch(err.requestOptions);
        return handler.resolve(response);
      } catch (e) {
        return handler.next(err);
      }
    }
    
    return handler.next(err);
  }
}
```

## Best Practices

1. **Single Instance**: Create one Dio instance per API
```dart
class ApiClient {
  static final Dio _dio = Dio(BaseOptions(
    baseUrl: 'https://api.example.com',
  ));
  
  static Dio get instance => _dio;
}
```

2. **Error Handling**: Always handle DioException
```dart
try {
  final response = await dio.get('/users');
  return response.data;
} on DioException catch (e) {
  switch (e.type) {
    case DioExceptionType.connectionTimeout:
      throw TimeoutException('Connection timeout');
    case DioExceptionType.receiveTimeout:
      throw TimeoutException('Receive timeout');
    case DioExceptionType.badResponse:
      throw ApiException(e.response?.statusCode);
    default:
      throw NetworkException(e.message);
  }
}
```

3. **Type Safety**: Parse responses to models
```dart
final response = await dio.get<Map<String, dynamic>>('/user/1');
final user = User.fromJson(response.data!);
```

4. **Cancellation**: Provide cancel tokens for long requests

5. **Testing**: Use mocks for testing
```dart
// Using mockito
final mockDio = MockDio();
when(mockDio.get('/users'))
    .thenAnswer((_) async => Response(data: [], statusCode: 200));
```

## Performance Tips

- Reuse Dio instances (don't create new ones per request)
- Set appropriate timeouts
- Use HTTP/2 adapter for better performance
- Enable gzip compression
- Cache responses when appropriate

## Resources

- **Official Documentation**: https://pub.dev/packages/dio
- **GitHub Repository**: https://github.com/cfug/dio
- **Examples**: https://github.com/cfug/dio/tree/main/example
- **API Reference**: https://pub.dev/documentation/dio/latest/

## Alternatives

- **http**: Simpler, official Dart HTTP client
- **Chopper**: Type-safe HTTP client generator
- **Retrofit**: Annotation-based HTTP client

---

**Last Updated**: October 14, 2025  
**Update Priority**: None (already latest)

