package ntu.ltcl.hanlp;

import java.io.IOException;
import java.net.InetSocketAddress;

import com.sun.net.httpserver.HttpServer;

public class HanLPhttp {

  public static void main(String[] args) throws Exception {
    int port = 1234;
    if (args.length > 0)
      port = Integer.parseInt(args[0]);
    HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);

    server.createContext("/test", new TestHandler());
    server.createContext("/test/", new TestHandler());

    server.createContext("/name", new NameHandler());
    server.createContext("/name/", new NameHandler());

    server.createContext("/translated_name", new TranslatedNameHandler());
    server.createContext("/translated_name/", new TranslatedNameHandler());

    server.createContext("/japanese_name", new JapaneseNameHandler());
    server.createContext("/japanese_name/", new JapaneseNameHandler());

    server.createContext("/place", new PlaceHandler());
    server.createContext("/place/", new PlaceHandler());

    server.setExecutor(null);

    server.start();
  }

}
