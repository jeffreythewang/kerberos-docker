import java.sql.*;
import java.util.Properties;

class KerberosPresto {
    public static void main(String[] args) {
        String url = "jdbc:presto://10.5.0.5:7778/jmx/current";
        Properties props = new Properties();
        props.setProperty("user", "jeffreyw");
        props.setProperty("SSL", "true");
        props.setProperty("SSLKeyStorePath", "/etc/presto_keystore.jks");
        props.setProperty("SSLKeyStorePassword", "prestodb");
        props.setProperty("KerberosRemoteServiceName", "presto");
        props.setProperty("KerberosPrincipal", "jeffreyw@EXAMPLE.COM");
        props.setProperty("KerberosConfigPath", "/etc/krb5.conf");
        props.setProperty("KerberosKeytabPath", "/etc/krb5.keytab");
        try {
            Connection conn = DriverManager.getConnection(url, props);
            Statement stmt = conn.createStatement();
            try {
                  ResultSet rs = stmt.executeQuery("SELECT * FROM \"java.lang:type=classloading\"");
                  while (rs.next()) {
                      String node = rs.getString(1);
                      System.out.println(node);
                  }
            } finally {
                stmt.close();
                conn.close();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
