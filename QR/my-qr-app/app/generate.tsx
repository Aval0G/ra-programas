import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';
import { Picker } from '@react-native-picker/picker';
import { barcodeToSvg } from '@adrianso/react-native-barcode-builder';
import Svg, { Path } from 'react-native-svg';
import QRCode from 'react-native-qrcode-svg';

// Formatos de códigos de barras y QR
const barcodeFormats = ['CODE39', 'CODE128', 'ITF', 'codabar', 'GenericBarcode', 'pharmacode'] as const;
const qrFormats = ['QRCode', 'MicroQRCode', 'QRCodeModel2'] as const;

type ValidBarcodeFormat = (typeof barcodeFormats)[number];
type ValidQRFormat = (typeof qrFormats)[number];

export default function Generate() {
  const [text, setText] = useState('');
  const [selectedCode, setSelectedCode] = useState<string>('');
  const [svgCode, setSvgCode] = useState<string>('');
  const [qrCode, setQrCode] = useState<JSX.Element | null>(null);

  // Validación para códigos de barras
  const validateBarcodeInput = (): boolean => {
    if (!text) {
      alert('Por favor ingrese el texto para generar el código.');
      return false;
    }

    switch (selectedCode) {
      case 'ITF':
        if (!/^[0-9]+$/.test(text) || text.length % 2 !== 0) {
          alert('El código ITF debe tener solo números y una longitud par.');
          return false;
        }
        break;
      case 'codabar':
        if (!/^[A-D0-9\$/\.\+\-]*$/.test(text)) {
          alert('El código Codabar solo permite números, A-D y los caracteres especiales $ / . + -.');
          return false;
        }
        break;
      case 'GenericBarcode':
        // No hay validación especial para GenericBarcode
        break;
      case 'pharmacode':
        if (!/^[0-9]{1,6}$/.test(text)) {
          alert('El código Pharmacode debe tener entre 1 y 6 dígitos numéricos.');
          return false;
        }
        break;
      case 'CODE39':
        if (!/^[A-Z0-9\-\. \$/\+%]*$/.test(text)) {
          alert('El código CODE39 solo permite letras mayúsculas, números y algunos caracteres especiales (- . $ / + %).');
          return false;
        }
        break;
      default:
        break;
    }
    return true;
  };

  // Validación para los códigos QR
  const validateQRInput = (): boolean => {
    if (!text.trim()) {
      alert('El contenido del QR no puede estar vacío.');
      return false;
    }
    return true;
  };

  // Función para generar códigos de barras
  const generateBarcodeCode = (): void => {
    if (!validateBarcodeInput()) return;
    try {
      const svg = barcodeToSvg({ value: text, format: selectedCode as ValidBarcodeFormat });
      setSvgCode(svg);
      setQrCode(null); // Limpiamos cualquier código QR generado previamente
    } catch (error) {
      alert('Error al generar el código de barras: ' + error);
    }
  };

  // Función para generar códigos QR
  const generateQRCode = (): void => {
    if (!validateQRInput()) return;
    setQrCode(
      <QRCode
        value={text}
        size={200}
        color="black"
        backgroundColor="white"
      />
    );
    setSvgCode(''); // Limpiamos cualquier código de barras generado previamente
  };

  // Función general para gestionar la generación según el tipo
  const generateCode = () => {
    if (!selectedCode) {
      alert('Debe seleccionar un tipo de código.');
      return;
    }

    if (barcodeFormats.includes(selectedCode as ValidBarcodeFormat)) {
      generateBarcodeCode(); // Genera un código de barras
    } else if (qrFormats.includes(selectedCode as ValidQRFormat)) {
      generateQRCode(); // Genera un código QR
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Generador de Códigos de Barras y QR</Text>
      <TextInput
        style={styles.input}
        placeholder="Ingrese el texto"
        value={text}
        onChangeText={setText}
      />
      <Picker
        selectedValue={selectedCode}
        style={styles.picker}
        onValueChange={(itemValue) => setSelectedCode(itemValue)}
      >
        <Picker.Item label="Seleccionar tipo de código (Ninguno)" value="" />
        <Picker.Item label="Código de Barras: CODE39" value="CODE39" />
        <Picker.Item label="Código de Barras: CODE128" value="CODE128" />
        <Picker.Item label="Código de Barras: ITF" value="ITF" />
        <Picker.Item label="Código de Barras: Codabar" value="codabar" />
        <Picker.Item label="Código de Barras: GenericBarcode" value="GenericBarcode" />
        <Picker.Item label="Código de Barras: Pharmacode" value="pharmacode" />
        <Picker.Item label="Código QR: QRCode" value="QRCode" />
        <Picker.Item label="Código QR: MicroQRCode" value="MicroQRCode" />
        <Picker.Item label="Código QR: QRCodeModel2" value="QRCodeModel2" />
      </Picker>
      <Button title="Generar Código" onPress={generateCode} />
      {svgCode ? (
        <View style={styles.codeContainer}>
          <Svg width={200} height={100} viewBox="0 0 200 100">
            <Path d={svgCode.match(/<path d="(.*?)"/i)?.[1]} fill="#000" />
          </Svg>
        </View>
      ) : qrCode ? (
        <View style={styles.codeContainer}>{qrCode}</View>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  title: { fontSize: 24, fontWeight: 'bold' },
  input: { width: 250, padding: 10, marginVertical: 20, borderWidth: 1, borderRadius: 5 },
  picker: { width: 250, marginVertical: 20 },
  codeContainer: { marginTop: 20 },
});
