import { useRouter, useLocalSearchParams } from "expo-router";
import { View, Text, Button, StyleSheet, Linking } from "react-native";

export default function ShowCode() {
    const router = useRouter();
    const { data } = useLocalSearchParams<{ data: string }>();

    const isValidUrl = (string: string) => {
        try {
            new URL(string);
            return true;
        } catch {
            return false;
        }
    };

    const handleOpenLink = () => {
        if (data && isValidUrl(data)) Linking.openURL(data);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.code}>Código Escaneado:</Text>
            {data && isValidUrl(data) ? (
                <Text style={styles.link} onPress={handleOpenLink}>
                    {data}
                </Text>
            ) : (
                <Text style={styles.plainText}>{data}</Text>
            )}
            <Button title="Escanear un nuevo código" onPress={() => router.push("/scan")} />
            <Button title="Volver al inicio" onPress={() => router.push("/")} />
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        padding: 20,
    },
    code: {
        fontSize: 20,
        marginBottom: 20,
    },
    link: {
        fontSize: 18,
        color: "blue",
        marginBottom: 40,
    },
    plainText: {
        fontSize: 18,
        marginBottom: 40,
    },
});
