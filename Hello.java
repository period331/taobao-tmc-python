import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.Arrays;
import java.security.MessageDigest;
import java.security.GeneralSecurityException;
import java.io.IOException;
import java.io.PrintStream;
import java.io.ByteArrayOutputStream;

public class Hello {
    public static void main(String[] args) throws IOException {
        Map<String, String> signHeader = new HashMap<String, String>();
        signHeader.put("timestamp", "1393999435452");
        signHeader.put("app_key", "1021737885");
        signHeader.put("group_name", "default");

        try {
            String sign = signTopRequestNew(signHeader, "sandboxbbf5579605d7936422c11af0e", false);    
        } catch (IOException e) {
            String msg = getStringFromException(e);
            throw new IOException(msg);
        }

        System.out.println("Hello world");
    }

    public static String signTopRequestNew(Map<String, String> params, String secret, boolean isHmac) throws IOException {
        // 第一步：检查参数是否已经排序
        String[] keys = params.keySet().toArray(new String[0]);
        Arrays.sort(keys);

        // 第二步：把所有参数名和参数值串在一起
        StringBuilder query = new StringBuilder();
        if (!isHmac) {
            query.append(secret);
        }
        for (String key : keys) {
            String value = params.get(key);
            if (areNotEmpty(key, value)) {
                query.append(key).append(value);
            }
        }

        // 第三步：使用MD5/HMAC加密
        byte[] bytes;
        query.append(secret);
        bytes = encryptMD5(query.toString());

        System.out.println(byte2hex(bytes));

        // 第四步：把二进制转化为大写的十六进制
        return byte2hex(bytes);
    }

    /**
     * 检查指定的字符串列表是否不为空。
     */
    public static boolean areNotEmpty(String... values) {
        boolean result = true;
        if (values == null || values.length == 0) {
            result = false;
        } else {
            for (String value : values) {
                result &= !isEmpty(value);
            }
        }
        return result;
    }

    private static byte[] encryptMD5(String data) throws IOException {
        byte[] bytes = null;
        try {
            MessageDigest md = MessageDigest.getInstance("MD5");
            bytes = md.digest(data.getBytes("UTF-8"));
        } catch (GeneralSecurityException gse) {
            String msg = getStringFromException(gse);
            throw new IOException(msg);
        }
        return bytes;
    }

    private static String byte2hex(byte[] bytes) {
        StringBuilder sign = new StringBuilder();
        for (int i = 0; i < bytes.length; i++) {
            String hex = Integer.toHexString(bytes[i] & 0xFF);
            if (hex.length() == 1) {
                sign.append("0");
            }
            sign.append(hex.toUpperCase());
        }
        return sign.toString();
    }

    private static String getStringFromException(Throwable e) {
        String result = "";
        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        PrintStream ps = new PrintStream(bos);
        e.printStackTrace(ps);
        try {
            result = bos.toString("UTF-8");
        } catch (IOException ioe) {
        }
        return result;
    }

    public static boolean isEmpty(String value) {
        int strLen;
        if (value == null || (strLen = value.length()) == 0) {
            return true;
        }
        for (int i = 0; i < strLen; i++) {
            if ((Character.isWhitespace(value.charAt(i)) == false)) {
                return false;
            }
        }
        return true;
    }
}